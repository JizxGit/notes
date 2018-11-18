### 常见读取数据的方式以及优缺点

一般来说，我们使用TensorFlow进行数据读取的方式有以下4种：

- 预先把所有数据加载进内存

- 在每轮训练中使用原生Python代码读取一部分数据，然后使用feed_dict输入到计算图
- 利用Threading和Queues从TFRecord中分批次读取数据
- 使用Dataset API

方案1对于数据量不大的场景来说是足够简单而高效的，将数据直接内嵌到Graph中，再把Graph传入Session中运行。但是随着数据量的增长，势必会对有限的**内存空间带来极大的压力**，Graph的传输会遇到效率问题，甚至导致我们十分熟悉的OutOfMemoryError；

方案2可以一定程度上缓解了方案(1)的内存压力问题，但是由于在**单线程环境下我们的IO操作一般都是同步阻塞的**，势必会在一定程度上导致学习时间的增加，尤其是相同的数据需要重复多次读取的情况下；

而方案(3)和方案(4)都利用了我们的TFRecord，由于使用了多线程使得IO操作不再阻塞我们的模型训练，同时为了实现线程间的数据传输引入了Queues。



### 写入TFRecord file

#### １导入库

```python
import tensorflow as tf
import numpy as np
```

#### ２ 构建writer，用于写入数据

```python
writer = tf.python_io.TFRecordWriter('test.tfrecord')
```

#### 3  创建样本写入字典

一个一个样本 地 写入TFRecord file中。

先把每个样本中所有feature的信息和值存到字典中，key为feature名，value为feature值。

feature值需要转变成tensorflow指定的feature类型中的一个：

- int64：`tf.train.Feature(int64_list = tf.train.Int64List(value=[输入]))`

- float32：`tf.train.Feature(float_list = tf.train.FloatList(value=[输入]))`

- string：`tf.train.Feature(bytes_list=tf.train.BytesList(value=[输入]))`

  > 注：value必须是list(向量)



如何处理类型是张量的feature

tensorflow **feature类型只接受list数据**，但如果数据类型是矩阵或者张量该如何处理？

两种方式：

- 转成list类型：将张量**fatten成list**(也就是向量)，再用写入list的方式写入。

- 转成string类型：将张量用**tostring()转换成string类型**，再用tf.train.Feature(bytes_list=tf.train.BytesList(value=[input.tostring()]))来存储。

形状信息：**不管那种方式都会使数据丢失形状信息**，所以在向该样本中写入feature时应该**额外加入shape信息**作为额外feature。shape信息是int类型，这里我是用原feature名字+'_shape'来指定shape信息的feature名。

```python
# 这里我们将会写3个样本，每个样本里有4个feature：标量，向量，矩阵，张量
for i in range(3):
    # 创建字典
    features={}
    # 写入标量，类型Int64，由于是标量，所以"value=[scalars[i]]" 变成list
    features['scalar'] = 
    tf.train.Feature(int64_list=tf.train.Int64List(value=[scalars[i]]))
    
    # 写入向量，类型float，本身就是list，所以"value=vectors[i]"没有中括号
    features['vector'] = 
    tf.train.Feature(float_list = tf.train.FloatList(value=vectors[i]))
    
    # 写入矩阵，类型float，本身是矩阵，一种方法是将矩阵flatten成list
    features['matrix'] = 
    tf.train.Feature(float_list = tf.train.FloatList(value=matrices[i].reshape(-1)))
    # 然而矩阵的形状信息(2,3)会丢失，需要存储形状信息，随后可转回原形状
    features['matrix_shape'] = 
    tf.train.Feature(int64_list = tf.train.Int64List(value=matrices[i].shape))
    
    # 写入张量，类型float，本身是三维张量，另一种方法是转变成字符类型存储，随后再转回原类型
    features['tensor']= 
    tf.train.Feature(bytes_list=tf.train.BytesList(value=[tensors[i].tostring()]))
    # 存储丢失的形状信息(806,806,3)
    features['tensor_shape'] = 
    tf.train.Feature(int64_list = tf.train.Int64List(value=tensors[i].shape))
```

3. 转成tf_features

    将存有所有feature的字典送入tf.train.Features中，相当于一条数据

    ```python
    tf_features = tf.train.Features(feature= features)
    ```

4. 转成tf_example

    再将其变成一个样本example

    ```python
    tf_example = tf.train.Example(features = tf_features)
    ```

5. 序列化样本

    ```python
    tf_serialized = tf_example.SerializeToString()
    ```

6. 写入样本

    写入一个序列化的样本

    ```python
    writer.write(tf_serialized)
    # 由于上面有循环3次，所以到此我们已经写了3个样本
    ```

7. 关闭TFRecord file

    ```python
    writer.close()
    ```

完整例子：

```python
import tensorflow as tf
import numpy as np
writer = tf.python_io.TFRecordWriter('test.tfrecord')

scalars = np.array([1,2,3],dtype=np.int64)

vectors = np.array([[0.1,0.1,0.1],
                   [0.2,0.2,0.2],
                   [0.3,0.3,0.3]],dtype=np.float32)

matrices = np.array([np.array((vectors[0],vectors[0])),
                    np.array((vectors[1],vectors[1])),
					np.array((vectors[2],vectors[2]))],dtype=np.float32)

tensors = np.array([np.array((matrices[0],matrices[0])),
                    np.array((matrices[1],matrices[1])),
					np.array((matrices[2],matrices[2]))],dtype=np.float32)

writer = tf.python_io.TFRecordWriter('test.tfrecord')

for i in range(3):
    # 创建字典
    features = {}
    # 写入标量，类型Int64，由于是标量，所以"value=[scalars[i]]" 变成list
    features['scalar'] =tf.train.Feature(int64_list=tf.train.Int64List(value=[scalars[i]]))

    # 写入向量，类型float，本身就是list，所以"value=vectors[i]"没有中括号
    features['vector'] =tf.train.Feature(float_list=tf.train.FloatList(value=vectors[i]))

    # 写入矩阵，类型float，本身是矩阵，一种方法是将矩阵flatten成list
    features['matrix'] =tf.train.Feature(float_list=tf.train.FloatList(value=matrices[i].reshape(-1)))
    # 然而矩阵的形状信息(2,3)会丢失，需要存储形状信息，随后可转回原形状
    features['matrix_shape'] =tf.train.Feature(int64_list=tf.train.Int64List(value=matrices[i].shape))

    # 写入张量，类型float，本身是三维张量，另一种方法是转变成字符类型存储，随后再转回原类型
    features['tensor'] =tf.train.Feature(bytes_list=tf.train.BytesList(value=[tensors[i].tostring()]))
    # 存储丢失的形状信息
    features['tensor_shape'] =tf.train.Feature(int64_list=tf.train.Int64List(value=tensors[i].shape))
    
    # 封装为一条数据
    tf_features=tf.train.Features(feature=features)
    tf_example = tf.train.Example(features=tf_features)
    tf_serialized = tf_example.SerializeToString()
    writer.write(tf_serialized)
writer.close()
```



### 确认TFRecord的内容

想确认下刚才生成的TFRecord是否合乎我们的预期，**tf.train.Example.FromString**应该是不二之选了。

```python
import tensorflow as tf

example = next(tf.python_io.tf_record_iterator("test.tfrecord"))
print(tf.train.Example.FromString(example))
```



### 读取TFRecord数据

#### 使用dataset api

从多个tfrecord文件中导入数据到Dataset类 （这里用两个一样）

```python
filenames = ["test.tfrecord", "test.tfrecord"]
dataset = tf.data.TFRecordDataset(filenames)
```

#### 解析数据

为了完成这项任务，推荐使用**tf.parse_single_example**：

由于从tfrecord文件中导入的样本是刚才写入的tf_serialized序列化样本，所以我们需要对每一个样本进行解析。这里就用`dataset.map(parse_function)`来对dataset里的每个样本进行相同的解析操作。

```python
def parse_function(example):
    # step 1：构造解析字典[1]
    features_dics = {
        # 这里没用default_value，随后的都是None
        'scalar': tf.FixedLenFeature(shape=(), dtype=tf.int64, default_value=None),

        # vector的shape刻意从原本的(3,)指定成(1,3)
        'vector': tf.FixedLenFeature(shape=(1, 3), dtype=tf.float32),

        # 使用 VarLenFeature来解析
        'matrix': tf.VarLenFeature(dtype=tf.float32),
        'matrix_shape': tf.FixedLenFeature(shape=(2,), dtype=tf.int64),

        # tensor在写入时 使用了toString()，shape是()
        # 但这里的type不是tensor的原type，而是字符化后所用的tf.string，随后再回转成原tf.uint8类型
        'tensor': tf.FixedLenFeature(shape=(), dtype=tf.string),
        'tensor_shape': tf.FixedLenFeature(shape=(3,), dtype=tf.int64)
    }

    # step 2：把序列化样本和解析字典送入函数里得到解析的样本
    parsed_example = tf.parse_single_example(example, features_dics)
    
    # step 3：转变特征[2]
  		# 解码字符
    parsed_example['tensor'] = tf.decode_raw(parsed_example['tensor'], tf.float32)
    	# 稀疏表示 转为 密集表示
    parsed_example['matrix'] = tf.sparse_tensor_to_dense(parsed_example['matrix'])
    
    # step 4：改变shape[3]
    	# 转变matrix形状
    parsed_example['matrix'] = tf.reshape(parsed_example['matrix'], parsed_example['matrix_shape'])
    
    	# 转变tensor形状
    parsed_example['tensor'] = tf.reshape(parsed_example['tensor'], parsed_example['tensor_shape'])
    
    # 返回所有feature
    return parsed_example
```

解析基本就是写入时的逆过程，所以在解析函数中会需要写入时的信息。

##### Step1 解析方式

- **定长特征**解析：`tf.FixedLenFeature(shape, dtype, default_value)`

  - shape：可当reshape来用，如下面例子中：vector的shape从(3,)改动成了(1,3)。

    > 注：如果写入的feature使用了.tostring() 其shape就是()

  - dtype：必须是tf.float32， tf.int64， tf.string中的一种。

  - default_value：feature值缺失时所指定的值。 

- **不定长特征**解析：`tf.VarLenFeature(dtype)`
  可以不明确指定shape，但得到的tensor是SparseTensor。

##### Step3 转变特征

得到的parsed_example也是一个字典，其中每个key是对应feature的名字，value是相应的feature解析值。如果使用了下面两种情况，则还需要对这些值进行转变。其他情况则不用。

- string类型：tf.decode_raw(parsed_feature, type) 来解码
  注：这里type必须要和当初.tostring()化前的一致。如tensor转变前是tf.uint8，这里就需是tf.uint8；转变前是tf.float32，则tf.float32
- VarLenFeature解析：由于得到的是SparseTensor，所以视情况需要用tf.sparse_tensor_to_dense(SparseTensor)来转变成DenseTensor

##### Step4 改变shape

到此为止得到的特征都是向量，需要根据之前存储的shape信息对每个feature进行reshape。



#### 获取数据

创建好解析函数后，将创建的`parse_function`送入`dataset.map()`得到新的数据集

```python
dataset = dataset.map(parse_function)
```

有了 解析过的数据集后，接下来就是使用**迭代器**获取当中的样本。

```python
# 创建获取数据集中样本的迭代器
iterator = dataset.make_one_shot_iterator()
```

```python
# 获得下一个样本
next_element = iterator.get_next()

with tf.Session() as sess:
    # 获取
    i = 1
    while True:
        # 不断的获得下一个样本
        try:
            # 获得的值直接属于graph的一部分，所以不再需要用feed_dict来喂
            scalar, vector, matrix, tensor = sess.run([next_element['scalar'],
                                                       next_element['vector'],
                                                       next_element['matrix'],
                                                       next_element['tensor']])
            # 如果遍历完了数据集，则返回错误
        except tf.errors.OutOfRangeError:
            print("End of dataset")
            break
        else:
            # 显示每个样本中的所有feature的信息，只显示scalar的值
            print('==============example %s ==============' % i)
            print('scalar: value: %s | shape: %s | type: %s' % (scalar, scalar.shape, scalar.dtype))
            print('vector: value: %s | shape: %s | type: %s' % (vector,vector.shape, vector.dtype))
            print('matrix value: %s | shape: %s | type: %s' % (matrix,matrix.shape, matrix.dtype))
            print('tensor value: %s | shape: %s | type: %s' % (tensor,tensor.shape, tensor.dtype))
        i += 1
```



参考：[TensorFlow中层API：Datasets+TFRecord的数据导入](https://zhuanlan.zhihu.com/p/33223782)

