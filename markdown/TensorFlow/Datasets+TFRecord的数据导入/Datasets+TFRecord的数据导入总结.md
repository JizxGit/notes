### 迭代器

构建了表示输入数据的 `Dataset` 后，下一步就是创建 `Iterator` 来访问该数据集中的元素。[`tf.data`](https://tensorflow.google.cn/api_docs/python/tf/data) API 目前支持下列迭代器，复杂程度逐渐增大：

- **单次**：`dataset.make_one_shot_iterator()`
- **可初始化** ：`dataset.make_initializable_iterator()`
- **可重新初始化**：`tf.data.Iterator.from_structure(training_dataset.output_types,training_dataset.output_shapes)`
- **可馈送**：`tf.data.Iterator.from_string_handle(handle, training_dataset.output_types, training_dataset.output_shapes)`

**单次**：

```python
dataset = tf.data.Dataset.range(100)
# 单次
iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

for i in range(100):
  value = sess.run(next_element)
  assert i == value
```

**可初始化**:

您需要先运行显式 `iterator.initializer` 操作，然后才能使用**可初始化**迭代器。虽然有些不便，但它允许您使用一个或多个 `tf.placeholder()` 张量（可在初始化迭代器时馈送）参数化数据集的定义

```python
max_value = tf.placeholder(tf.int64, shape=[])
dataset = tf.data.Dataset.range(max_value)
# 可初始化
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()

# 使用10初始化dataset的迭代器
sess.run(iterator.initializer, feed_dict={max_value: 10})
for i in range(10):
  value = sess.run(next_element)
  assert i == value

# 使用100初始化dataset的迭代器
sess.run(iterator.initializer, feed_dict={max_value: 100})
for i in range(100):
  value = sess.run(next_element)
  assert i == value
```

**可重新初始化**：

> 优点：不同数据集**共用**同一个iterator

迭代器（iterator）可以通过多个不同的 `Dataset` 对象进行初始化。例如，您可能有一个**训练输入**管道，它会对输入图片进行随机扰动来改善泛化；还有一个**验证输入**管道，它会评估对未修改数据的预测。这些管道通常会使用不同的 `Dataset`对象，这些对象具有相同的结构（即每个组件具有相同类型和兼容形状）。

```python
# Define training and validation datasets with the same structure.
training_dataset = tf.data.Dataset.range(100).map(
    lambda x: x + tf.random_uniform([], -10, 10, tf.int64))
validation_dataset = tf.data.Dataset.range(50)

# A reinitializable iterator is defined by its structure. We could use the
# `output_types` and `output_shapes` properties of either `training_dataset`
# or `validation_dataset` here, because they are compatible.
iterator = tf.data.Iterator.from_structure(training_dataset.output_types,
                                           training_dataset.output_shapes)
next_element = iterator.get_next()

# 这里只是定义初始化的操作，通过sess.run才真正进行了数据集的切换
training_init_op = iterator.make_initializer(training_dataset)
validation_init_op = iterator.make_initializer(validation_dataset)

# Run 20 epochs in which the training dataset is traversed, followed by the
# validation dataset.
for _ in range(20):
  # 使用训练数据集初始化 iterator
  sess.run(training_init_op)
  for _ in range(100):
    sess.run(next_element)

  # 使用验证数据集初始化 iterator
  sess.run(validation_init_op)
  for _ in range(50):
    sess.run(next_element)
```



**可馈送**迭代器可以与 [`tf.placeholder`](https://tensorflow.google.cn/api_docs/python/tf/placeholder) 一起使用，通过熟悉的 `feed_dict` 机制选择每次调用 [`tf.Session.run`](https://tensorflow.google.cn/api_docs/python/tf/InteractiveSession#run) 时所使用的 `Iterator`。

> 优点：它提供的功能与可重新初始化迭代器的相同，但**在迭代器之间切换时不需要从数据集的开头初始化迭代器**。

例如，以上面的同一训练和验证数据集为例，您可以使用 [`tf.data.Iterator.from_string_handle`](https://tensorflow.google.cn/api_docs/python/tf/data/Iterator#from_string_handle) 定义一个可让您在两个数据集之间切换的可馈送迭代器：

```python
# Define training and validation datasets with the same structure.
training_dataset = tf.data.Dataset.range(100).map(
    lambda x: x + tf.random_uniform([], -10, 10, tf.int64)).repeat()
validation_dataset = tf.data.Dataset.range(50)

# 使用一个handle placeholder 和数据集的structure定义一个feedable iterator 
handle = tf.placeholder(tf.string, shape=[])
iterator = tf.data.Iterator.from_string_handle(
    handle, training_dataset.output_types, training_dataset.output_shapes)
next_element = iterator.get_next()

# 使用feedable iterators时可以组合不同的iterator
training_iterator = training_dataset.make_one_shot_iterator()
validation_iterator = validation_dataset.make_initializable_iterator()

# `Iterator.string_handle()` 返回一个tensor，这个tensor能够被验证并用于上面定义的`handle` placeholder.
training_handle = sess.run(training_iterator.string_handle())
validation_handle = sess.run(validation_iterator.string_handle())

# Loop forever, alternating between training and validation.
while True:
  # Run 200 steps using the training dataset. Note that the training dataset is
  # infinite, and we resume from where we left off in the previous `while` loop
  # iteration.
  for _ in range(200):
    sess.run(next_element, feed_dict={handle: training_handle})

  # Run one pass over the validation dataset.
  sess.run(validation_iterator.initializer)
  for _ in range(50):
    sess.run(next_element, feed_dict={handle: validation_handle})
```


### 消耗 TFRecord 数据

[`tf.data`](https://tensorflow.google.cn/api_docs/python/tf/data) API 支持多种文件格式，因此您可以处理那些不适合存储在内存中的大型数据集。例如，TFRecord 文件格式是一种面向记录的简单二进制格式，很多 TensorFlow 应用采用此格式来训练数据。

```
# Creates a dataset that reads all of the examples from two files.
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
```

`TFRecordDataset` 初始化程序的 `filenames` 参数可以是**字符串、字符串列表，也可以是字符串 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor)**。因此，如果您有两组分别用于训练和验证的文件，则可以使用 `tf.placeholder(tf.string)` 来表示文件名，并使用适当的文件名初始化迭代器：

```python
filenames = tf.placeholder(tf.string, shape=[None])
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)  # 将record 解析为 tensors.
dataset = dataset.repeat()  # 将input重复无穷次.
dataset = dataset.batch(32)
iterator = dataset.make_initializable_iterator()

# You can feed the initializer with the appropriate filenames for the current
# phase of execution, e.g. training vs. validation.

# 将`iterator`初始化为训练数据
training_filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
sess.run(iterator.initializer, feed_dict={filenames: training_filenames})

# 将`iterator`初始化为验证数据
validation_filenames = ["/var/data/validation1.tfrecord", ...]
sess.run(iterator.initializer, feed_dict={filenames: validation_filenames})
```



### 使用 `Dataset.map()` 预处理数据

`Dataset.map(f)` 转换通过将解析函数 `f` 应用于输入数据集的每个元素来生成新数据集。函数 `f` 会接受表示输入中单个元素的 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor) 对象，并返回表示新数据集中单个元素的 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor) 对象。此函数的实现使用标准的 TensorFlow 指令将一个元素转换为另一个元素。

本部分介绍了如何使用 `Dataset.map()` 的常见示例。

#### 解析 `tf.Example` 协议缓冲区消息

许多输入管道都从 TFRecord 格式的文件（例如使用 [`tf.python_io.TFRecordWriter`](https://tensorflow.google.cn/api_docs/python/tf/python_io/TFRecordWriter) 编写而成）中提取 [`tf.train.Example`](https://tensorflow.google.cn/api_docs/python/tf/train/Example) 协议缓冲区消息。每个 [`tf.train.Example`](https://tensorflow.google.cn/api_docs/python/tf/train/Example) 记录都包含一个或多个“特征”，输入管道通常会将这些特征转换为张量。

```python
# Transforms a scalar string `example_proto` into a pair of a scalar string and
# a scalar integer, representing an image and its label, respectively.
def _parse_function(example_proto):
  # 指定解析的字段、默认值
  features = {"image": tf.FixedLenFeature((), tf.string, default_value=""),
              "label": tf.FixedLenFeature((), tf.int32, default_value=0)}
  # 从parse_single_example解析，获取还原后的训练数据
  parsed_features = tf.parse_single_example(example_proto, features)
  return parsed_features["image"], parsed_features["label"]

# Creates a dataset that reads all of the examples from two files, and extracts
# the image and label features.
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(_parse_function)
```



#### 使用 `tf.py_func()` 应用任意 Python 逻辑

```python
import cv2

# 使用自定义的方法来读取图像
def _read_py_function(filename, label):
  image_decoded = cv2.imread(filename.decode(), cv2.IMREAD_GRAYSCALE)
  return image_decoded, label

# 使用标准的TensorFlow操作将图片转为固定的shape.
def _resize_function(image_decoded, label):
  image_decoded.set_shape([None, None, None])
  image_resized = tf.image.resize_images(image_decoded, [28, 28])
  return image_resized, label

# 训练数据只指定图像文件名，在map解析函数中才真正读取、resize得到图像的tensor
filenames = ["/var/data/image1.jpg", "/var/data/image2.jpg", ...]
labels = [0, 37, 29, 1, ...]

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(
    lambda filename, label: tuple(tf.py_func(
        _read_py_function, [filename, label], [tf.uint8, label.dtype])))
dataset = dataset.map(_resize_function)
```



### 批处理

#### 简单的批处理

最简单的批处理形式是将数据集中的 `n` 个连续元素堆叠为一个元素。`Dataset.batch()` 转换正是这么做的，它与 `tf.stack()` 运算符具有相同的限制（被应用于元素的每个组件）：即对于每个组件 i，所有元素的张量形状必须完全相同。**

```
inc_dataset = tf.data.Dataset.range(100)
dec_dataset = tf.data.Dataset.range(0, -100, -1)
dataset = tf.data.Dataset.zip((inc_dataset, dec_dataset))
batched_dataset = dataset.batch(4)

iterator = batched_dataset.make_one_shot_iterator()
next_element = iterator.get_next()

print(sess.run(next_element))  # ==> ([0, 1, 2,   3],   [ 0, -1,  -2,  -3])
print(sess.run(next_element))  # ==> ([4, 5, 6,   7],   [-4, -5,  -6,  -7])
print(sess.run(next_element))  # ==> ([8, 9, 10, 11],   [-8, -9, -10, -11])
```



#### 使用填充批处理张量

```python
dataset = tf.data.Dataset.range(100)
dataset = dataset.map(lambda x: tf.fill([tf.cast(x, tf.int32)], x))
# 四个训练数据为一个batch，padded_shapes指定pad的固定长度，如果none的话就取一个batch中最长的长度，如果指定了长度，但是长度比batch中的某一个短的话会出错
dataset = dataset.padded_batch(4, padded_shapes=[None])

iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

print(sess.run(next_element))  # ==> [[0, 0, 0], [1, 0, 0], [2, 2, 0], [3, 3, 3]]
print(sess.run(next_element))  # ==> [[4, 4, 4, 4, 0, 0, 0],
                               #      [5, 5, 5, 5, 5, 0, 0],
                               #      [6, 6, 6, 6, 6, 6, 0],
                               #      [7, 7, 7, 7, 7, 7, 7]]
```



### 重复使用训练数据

要迭代数据集多个周期，最简单的方法是使用 `Dataset.repeat()` 转换。例如，要创建一个将其输入重复 10 个周期的数据集：

```python
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.repeat(10) # 重复次数
dataset = dataset.batch(32)
```

**应用不带参数的 `Dataset.repeat()` 转换将无限次地重复输入**。`Dataset.repeat()` 转换将其参数连接起来，而不会在一个周期结束和下一个周期开始时发出信号。

如果您想在每个周期结束时收到信号，则可以编写在数据集结束时捕获 [`tf.errors.OutOfRangeError`](https://tensorflow.google.cn/api_docs/python/tf/errors/OutOfRangeError) 的训练循环。此时，您可以收集关于该周期的一些统计信息（例如验证错误）。

```python
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.batch(32)
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()

# Compute for 100 epochs.
for _ in range(100):
  sess.run(iterator.initializer)
  while True:
    try:
      sess.run(next_element)
    except tf.errors.OutOfRangeError:
      break
```

### 打乱数据顺序

`Dataset.shuffle()` 转换会使用类似于 [`tf.RandomShuffleQueue`](https://tensorflow.google.cn/api_docs/python/tf/RandomShuffleQueue) 的算法随机重排输入数据集：它会维持一个固定大小的缓冲区，并**从该缓冲区统一地随机选择下一个元素**。

```python
filenames = ["/var/data/file1.tfrecord", "/var/data/file2.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
dataset = dataset.map(...)
dataset = dataset.shuffle(buffer_size=10000)
dataset = dataset.batch(32)
dataset = dataset.repeat()
```



