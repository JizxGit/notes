### 基本概念：Dataset、Iterator与元素

![dataset与iterator](./dataset与iterator.jpg)

我们只需要关注两个最重要的基础类：Dataset和Iterator。

Dataset可以看作是相同类型“**元素**”的有序列表。

**元素可以理解为一条训练数据**。在实际使用时，单个“元素”可以是向量，也可以是字符串、图片，甚至是tuple或者dict。

而Iterator是迭代获取dataset中数据的一种类。



### 从内存中创建复杂的Dataset与make_one_shot_iterator

通过from_tensor_slices可以构造一个dataset，它的真正作用是切分传入Tensor的第一个维度，生成相应的dataset

先以最简单的，Dataset的每一个元素是一个【数字】为例，

```python
import tensorflow as tf
import numpy as np
# 一共5条数据，每条数据是一个数字
dataset = tf.data.Dataset.from_tensor_slices(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
# 这个Iterator是一个“one shot iterator”，即只能从头到尾读取一次。
iterator = dataset.make_one_shot_iterator() 
one_element = iterator.get_next()
with tf.Session() as sess:
    try:
        while True:
            print(sess.run(one_element))
    except tf.errors.OutOfRangeError:
        print("end!")
```

```
1.0
2.0
3.0
4.0
5.0
end!
```



【矩阵】，每个元素还可以是一个向量

```python
...
# 一共5条数据，每条数据是一个2维的向量
dataset = tf.data.Dataset.from_tensor_slices(np.random.uniform(size=(5, 2)))
...
```

```
[0.06612407 0.82404996]
[0.10316804 0.59619761]
[0.99580047 0.16961195]
[0.32246138 0.95502333]
[0.57836463 0.10710992]
end!
```

【字典】

```python
...
# 一共5条数据，每条数据是一个字典，a对应一个数值，b对应一个向量
dataset = tf.data.Dataset.from_tensor_slices(
    {
        "a": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),                                       
        "b": np.random.uniform(size=(5, 2))
    }
)
...
```

```
{'a': 1.0, 'b': array([0.62259034, 0.48876187])}
{'a': 2.0, 'b': array([0.82547641, 0.68932993])}
{'a': 3.0, 'b': array([0.04185904, 0.8597056 ])}
{'a': 4.0, 'b': array([0.52579939, 0.23051884])}
{'a': 5.0, 'b': array([0.53255997, 0.53923747])}
end!
```



【元组】

```python
...

dataset = tf.data.Dataset.from_tensor_slices(
  (np.array([1.0, 2.0, 3.0, 4.0, 5.0]), np.random.uniform(size=(5, 2)))
)
...
```

```
(1.0, array([0.99204135, 0.85003613]))
(2.0, array([0.19624388, 0.86857535]))
(3.0, array([0.28657576, 0.9243944 ]))
(4.0, array([0.54961967, 0.74677561]))
(5.0, array([0.56485428, 0.63105195]))
end!
```



### 对Dataset中的元素做处理

一个Dataset通过Transformation**变成一个新的Dataset**。通常我们可以通过Transformation完成数据变换，打乱，组成batch，生成epoch等一系列操作。

常用的Transformation有：

- map(数据变换)
- batch
- shuffle(打乱)
- repeat(生成epoch)



1）map

map接收一个函数，Dataset中的每个元素都会被当作这个函数的输入，并将函数返回值组成新的Dataset

```python
dataset = tf.data.Dataset.from_tensor_slices(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
dataset = dataset.map(lambda x: x + 1) # 2.0, 3.0, 4.0, 5.0, 6.0
```

2）batch

batch就是将多个元素组合成batch，如下面的程序将dataset中的每个元素组成了大小为32的batch：

```python
dataset = dataset.shuffle(buffer_size=10000)
```

3）shuffle

shuffle的功能为打乱dataset中的元素，它有一个参数buffersize，表示打乱时使用的buffer的大小，我的理解是一次将10000个元素进行打乱：

```python
dataset = dataset.shuffle(buffer_size=10000)
```

4）repeat

repeat的功能就是将整个序列重复多次，主要用来处理机器学习中的epoch，假设原先的数据是一个epoch，使用repeat(5)就可以将之变成5个epoch：

```python 
dataset = dataset.repeat(5)
```

如果**直接调用repeat()的话**，生成的序列就**会无限重复下去**，没有结束，因此也不会抛出tf.errors.OutOfRangeError异常：

```python
dataset = dataset.repeat()
```



### 例子：读入磁盘图片与对应label

```python
# 函数的功能时将filename对应的图片文件读进来，并缩放到统一的大小
def _parse_function(filename, label):
  image_string = tf.read_file(filename)
  image_decoded = tf.image.decode_image(image_string)
  image_resized = tf.image.resize_images(image_decoded, [28, 28])
  return image_resized, label
 
# 图片文件的列表
filenames = tf.constant(["/var/data/image1.jpg", "/var/data/image2.jpg", ...])
# label[i]就是图片filenames[i]的label
labels = tf.constant([0, 37, ...])
 
# 此时dataset中的一个元素是(filename, label)
dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
 
# 此时dataset中的一个元素是(image_resized, label),得到了真正的图片数据
dataset = dataset.map(_parse_function)
 
# 此时dataset中的一个元素是(image_resized_batch, label_batch)
dataset = dataset.shuffle(buffersize=1000).batch(32).repeat(10)
```

在这个过程中，dataset经历三次转变：

- 运`dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))`后，dataset的一个元素是(filename, label)。filename是图片的文件名，label是图片对应的标签。
- 之后**通过map**，将filename对应的图片读入，并缩放为28x28的大小。此时dataset中的一个元素是(image_resized, label)
- 最后，`dataset.shuffle(buffersize=1000).batch(32).repeat(10)`的功能是：在每个epoch内将图片打乱组成大小为32的batch，并重复10次。
- 最终，dataset中的一个元素是(image_resized_batch, label_batch)，image_resized_batch的形状为(32, 28, 28, 3)，而label_batch的形状为(32, )，接下来我们就可以用这两个Tensor来建立模型了。



###  Dataset的其它创建方法

除了tf.data.Dataset.from_tensor_slices外，目前Dataset API还提供了另外三种创建Dataset的方式：

- `tf.data.TextLineDataset()`：这个函数的输入是一个文件的列表，输出是一个dataset。dataset中的每一个元素就对应了文件中的一行。可以使用这个函数来读入CSV文件。
- `tf.data.FixedLengthRecordDataset()`：这个函数的输入是一个文件的列表和一个record_bytes，之后dataset的每一个元素就是文件中固定字节数record_bytes的内容。通常用来读取以二进制形式保存的文件，如CIFAR10数据集就是这种形式。
- `tf.data.TFRecordDataset()`：顾名思义，这个函数是用来读TFRecord文件的，dataset中的每一个元素就是一个TFExample。

#### tf.data.TFRecordDataset

具体参考这篇文章  [TFRecord](./TFRecord.md)

#### tf.data.Dataset.zip 组合多个dataset为一个

```python
# 每个元素是数值
dataset1 = tf.data.Dataset.from_tensor_slices(tf.fill([4],1))
# 每个元素的一个元组
dataset2 = tf.data.Dataset.from_tensor_slices((tf.fill([4,10],2), tf.fill([4, 20],3)))
# 将数值、元组拼起来成为一条新的数据
dataset3 = tf.data.Dataset.zip((dataset1, dataset2))

# iterator = dataset3.make_initializable_iterator()
# sess.run(iterator.initializer)
iterator = dataset3.make_one_shot_iterator()

next1, (next2, next3) = iterator.get_next()
for _ in range(4):
    a1,a2,a3=sess.run([next1,next2,next3])
    print(a1)
    print(a2)
    print(a3)
    print("*****")
```



### 更多类型的Iterator

在非Eager模式下，最简单的创建Iterator的方法就是通过dataset.make_one_shot_iterator()来创建一个one shot iterator。除了这种one shot iterator外，还有三个更复杂的Iterator，即：

- initializable iterator
- reinitializable iterator
- feedable iterator

#### 

#### initializable iterator

> dataset中有placeholder，使用前需要初始化

initializable iterator必须要在使用前通过sess.run()来初始化。

因为在dataset中使用了**placeholder**，在使用initializable iterator，可以将placeholder代入Iterator中，这可以**方便我们通过参数快速定义新的Iterator**。

```python
limit_placeholder = tf.placeholder(dtype=tf.int32, shape=[])
 
dataset = tf.data.Dataset.from_tensor_slices(tf.range(start=0, limit=limit_placeholder))
 
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()
 
with tf.Session() as sess:
    # 初始化一个Iterator
    max_value=10
    sess.run(iterator.initializer, feed_dict={limit_placeholder: max_value})
    for i in range(max_value):
      value = sess.run(next_element)
      assert i == value
        
    # 重新定义一个不同的Iterator 
    max_value=100
    sess.run(iterator.initializer, feed_dict={limit_placeholder: max_value})
    for i in range(max_value):
      value = sess.run(next_element)
      assert i == value
```

此时的limit相当于一个“参数”，它规定了Dataset中数的“上限”。



initializable iterator还有一个功能：读入较大的数组。

在使用`tf.data.Dataset.from_tensor_slices(array)`时，实际上发生的事情是**将 array 作为一个tf.constants保存到了计算图中**。当array很大时，会**导致计算图变得很大**，给传输、保存带来不便。

这时，我们可以用一个placeholder取代这里的array，并使用initializable iterator，只在需要时将array传进去，这样就可以**避免把大数组保存在图里**，示例代码为（来自官方例程）：

```python
# 从硬盘中读入两个Numpy数组
with np.load("/var/data/training_data.npy") as data:
  features = data["features"]
  labels = data["labels"]
 
features_placeholder = tf.placeholder(features.dtype, features.shape)
labels_placeholder = tf.placeholder(labels.dtype, labels.shape)
 
dataset = tf.data.Dataset.from_tensor_slices((features_placeholder, labels_placeholder))
iterator = dataset.make_initializable_iterator()
sess.run(iterator.initializer, feed_dict={features_placeholder: features,
                                          labels_placeholder: labels})
```



#### reinitializable iterator

> 直观理解：多个dataset可以通过同一个 iterator来进行迭代获取数据
>
> A reinitializable iterator can be initialized from multiple different Dataset objects. 

```python
# 定义有相同结构（structure）的训练数据集、验证数据集
training_dataset = tf.data.Dataset.range(100).map(
    lambda x: x + tf.random_uniform([], -10, 10, tf.int64))
validation_dataset = tf.data.Dataset.range(50)

# reinitializable iterator 由structure进行定义. 使用训练数据集或者验证数据集的
# `output_types` 和 `output_shapes` 来定义，因为他们是兼容的
iterator = tf.data.Iterator.from_structure(training_dataset.output_types,
                                           training_dataset.output_shapes)

training_iterator_init_op = iterator.make_initializer(training_dataset)
validation_iterator_init_op = iterator.make_initializer(validation_dataset)

next_element = iterator.get_next()

# Run 20 epochs 
# 每轮中训练数据集（training dataset）被遍历后， 紧接着遍历验证数据集（validation dataset）
for _ in range(20):
  # 初始化训练数据集的迭代器(iterator) 
  sess.run(training_iterator_init_op)
  for _ in range(100):
    print(sess.run(next_element))

  # 初始化验证数据集的迭代器(iterator) 
  sess.run(validation_iterator_init_op)
  for _ in range(50):
    print(sess.run(next_element))
```

#### Feedable iterator

Feedable iterator与tf.placeholder一起使用，来选择sess.run时用哪个迭代器（iterator）

使用`tf.data.Iterator.from_string_handle`来定义Feedable iterator，这个迭代器运行你在两个dataset之间切换

与reinitializable iterator很像，但是在不同dataset间切换时，它不要求你将迭代器 重新初始化为 从dataset第一条数据开始

```python
import tensorflow as tf

# 定义相同结构的训练数据集（training）和 验证数据集 （validation）
training_dataset = tf.data.Dataset.range(100).map(lambda x: x + 1).repeat() # 无限重复的数据
validation_dataset = tf.data.Dataset.range(50)

# 使用handle placeholder 和dataset的structure 来定义一个feedable iterator . We
# 任意使用训练数据集或者验证数据集的`output_types` and `output_shapes` 属性来定义 、
# 他们有相同的结构（structure）
handle = tf.placeholder(tf.string, shape=[]) # 用于填充具体dataset的iterator的数据,如下面的training_iterator
iterator = tf.data.Iterator.from_string_handle(handle, training_dataset.output_types, training_dataset.output_shapes)
next_element = iterator.get_next()

# feedable iterators 可以使用不同的iterator
# (比如 one-shot and initializable iterators).
training_iterator = training_dataset.make_one_shot_iterator()
validation_iterator = validation_dataset.make_initializable_iterator()

with tf.Session() as sess:
    # `Iterator.string_handle()` 方法返回一个 tensor ，用于feed `handle` placeholder.
    training_data_handle = sess.run(training_iterator.string_handle())
    validation_data_handle = sess.run(validation_iterator.string_handle())
    # Loop forever, alternating between training and validation.
    for _ in range(10):
        # 训练数据集上跑50steps，然后切换到验证数据集，下次获取训练数据时，是从上一次for循环离开时的位置继续跑50step
        print("********训练数据*********")
        for _ in range(50):
            print(sess.run(next_element, feed_dict={handle: training_data_handle}))
        # 跑一遍全部的验证数据集
        sess.run(validation_iterator.initializer)
        print("--------验证数据---------")
        for _ in range(50):
            print(sess.run(next_element, feed_dict={handle: validation_data_handle}))
```



### 保存iterator

```python
# 将 iterator 转为 saveable object
saveable = tf.contrib.data.make_saveable_from_iterator(iterator)

# Save the iterator state by adding it to the saveable objects collection.
# 通过将 saveable 加入到 tf.GraphKeys.SAVEABLE_OBJECTS 集合中，保存iterator的状态
tf.add_to_collection(tf.GraphKeys.SAVEABLE_OBJECTS, saveable)
saver = tf.train.Saver()

with tf.Session() as sess:

  if should_checkpoint:
    saver.save(path_to_checkpoint)

# 恢复 iterator 状态.
with tf.Session() as sess:
  saver.restore(sess, path_to_checkpoint)
```

