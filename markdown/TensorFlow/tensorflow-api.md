### 输出

tf.nn.softmax_cross_entropy_with_logits(记为**f1**) 
tf.nn.softmax_cross_entropy_with_logits_v2(记为**f2**) tf.nn.sparse_softmax_cross_entropy_with_logits(记为**f3**),之间的区别。

f1和f3对于参数logits的要求都是一样的，即未经处理的，直接由神经网络输出的数值， 比如 [3.5,2.1,7.89,4.4]。两个函数不一样的地方在于labels格式的要求，**f1的要求labels的格式和logits类似，比如[0,0,1,0]**。而**f3的要求labels是一个数值**，这个数值记录着ground truth所在的索引。以[0,0,1,0]为例，这里真值1的索引为2。所以f3要求labels的输入为数字2(tensor)。一般可以用tf.argmax()来从[0,0,1,0]中取得真值的索引。

f1和f2之间很像，实际上官方文档已经标记出**f1已经是deprecated状态，推荐使用f2**。

两者唯一的区别在于f1在进行反向传播的时候，只对logits进行反向传播，labels保持不变。而f2在进行反向传播的时候，同时对logits和labels都进行反向传播，如果将labels传入的tensor设置为stop_gradients，就和f1一样了。 
那么问题来了，一般我们在进行监督学习的时候，labels都是标记好的真值，什么时候会需要改变label？f2存在的意义是什么？实际上在应用中labels并不一定都是人工手动标注的，有的时候还可能是神经网络生成的，一个实际的例子就是对抗生成网络（GAN）。

测试用代码：

```python
import tensorflow as tf

import numpy as np

Truth = np.array([0,0,1,0])

Pred_logits = np.array([3.5,2.1,7.89,4.4])

loss = tf.nn.softmax_cross_entropy_with_logits(labels=Truth,logits=Pred_logits)

loss2 = tf.nn.softmax_cross_entropy_with_logits_v2(labels=Truth,logits=Pred_logits)

loss3 = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=tf.argmax(Truth),logits=Pred_logits)

with tf.Session() as sess:
    print(sess.run(loss))
    print(sess.run(loss2))
    print(sess.run(loss3))
```



### RNN

#### BasicLSTMCell的输出

BasicLSTMCell的state有两个部分，memory cell和hidden state。使用dynamic_rnn，返回两个输出，outputs和state。outputs是每个 time step的hidden state，而state就是最后一个time step的memory cell 和hidden state。如果你指的所有时刻的state是hidden state的话，那么outputs就可以了。

作者：Frank小四链接：https://www.zhihu.com/question/58417377/answer/193747914来源：知乎著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### 乘法

####  tf.diag_part 取对角线

```
diag_part(
    input,
    name=None
)1234
```

返回张量的对角线部分。



#### tf.multiply 

（1）tf.multiply是点乘，即Returns x * y element-wise.

（2）tf.matmul是矩阵乘法，即Multiplies matrix a by matrix b, producing a * b.

#### tf.matmul

（1）tf.multiply是点乘，即Returns x * y element-wise.

（2）tf.matmul是**矩阵乘法**，`a:MxN, b:NxP, a*b:MxP` 即Multiplies matrix a by matrix b, producing a * b.

```
tf.matmul(a, b, 
	transpose_a=False, //将a矩阵转制
	transpose_b=False, //将b矩阵转制
	a_is_sparse=False, //a是否为稀疏矩阵，很多零
	b_is_sparse=False, //b是否为稀疏矩阵
	name=None)
```



#### tf.stack

```
tf.stack(
    values,
    axis=0,
    name='stack'
)
```

函数参数：

- values：具有相同形状和类型的 Tensor 对象列表。
- axis：一个 int，要一起堆叠的轴，默认为第一维，负值环绕，所以有效范围是[-(R+1), R+1)。
- name：此操作的名称（可选）。

将秩为 R 的张量列表堆叠成一个秩为 (R+1) 的张量。 

将 values 中的张量列表打包成一个张量，该张量比 values 中的每个张量都高一个秩，通过沿 axis 维度打包。给定一个形状为(A, B, C)的张量的长度 N 的列表；

如果 axis == 0，那么 output 张量将具有形状(N, A, B, C)。如果 axis == 1，那么 output 张量将具有形状(A, N, B, C)。

例如：

```
x = tf.constant([1, 4])
y = tf.constant([2, 5])
z = tf.constant([3, 6])
tf.stack([x, y, z])  # [[1, 4], [2, 5], [3, 6]] (Pack along first dim.)
tf.stack([x, y, z], axis=1)  # [[1, 2, 3], [4, 5, 6]]
```

####  tf.cast类型强转

tf.cast(x, dtype, name=None) ，tensor类型强转

The operation casts `x` (in case of `Tensor`) or `x.values` (in case of `SparseTensor`) to `dtype`.

For example:

```
# tensor `a` is [1.8, 2.2], dtype=tf.float
tf.cast(a, tf.int32) ==> [1, 2]  # dtype=tf.int32

```

 Args:

- **x**: A `Tensor` or `SparseTensor`.
- **dtype**: The destination type.
- **name**: A name for the operation (optional).




### 矩阵形状、变形

#### tf.rank 秩

Tensor的秩（有时也叫“序”(order)或者“度”(degree)又或者“n-维度”）是**tensor维度的数量**。例如，下面的tensor（定义为一个Python列表）的秩为2：

```
 t =[[1,2,3],[4,5,6],[7,8,9]]
```

Tensor的秩与矩阵的秩不一样。

Tensorflow文档使用三种惯用标记来描述tensor的维度：秩、形状和维数。下表这些标记相互之间的对应关系：

| 秩Rank | 形状 Shape           | 维度 Dimension number | Example                                 |
| ----- | ------------------ | ------------------- | --------------------------------------- |
| 0     | []                 | 0-D                 | A 0-D tensor. A scalar.                 |
| 1     | [D0]               | 1-D                 | A 1-D tensor with shape [5].            |
| 2     | [D0, D1]           | 2-D                 | A 2-D tensor with shape [3, 4].         |
| 3     | [D0, D1, D2]       | 3-D                 | A 3-D tensor with shape [1, 4, 3].      |
| n     | [D0, D1, ... Dn-1] | n-D                 | A tensor with shape [D0, D1, ... Dn-1]. |

#### tf.shape,tf.size,tf.rank

tf.shape 返回tensor的形状

```
# 't' is [[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]]
shape(t) ==> [2, 2, 3]
```

tf.size 返回 tensor中的元素数量

```
# 't' is [[[1, 1,, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]]]
size(t) ==> 12
```

tf.rank 返回tensor的维度，或者秩

```
# 't' is [[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]]
# shape of tensor 't' is [2, 2, 3]
rank(t) ==> 3
```

#### tf.shape与get_shape 的区别

相同点：都可以得到tensor a的尺寸

区别：

* ` a_shape=tf.shape(a)` , 输入的类型可以是tensor, list, array，返回一个tensor，**必须用sess.run(a_shape)才能得到结果** 
* `a_get_shape=a.get_shape()` 中a的数据类型**只能是tensor**,且返回值a_get_shape是一个元组（tuple），**能直接打印，不能用sess.run(a_get_shape)**

```python
x=tf.constant([[1,2,3],[4,5,6]])
y=[[1,2,3],[4,5,6]]
z=np.arange(24).reshape([2,3,4])
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    x_shape = tf.shape(x)  # x_shape 是一个tensor,[2 3]
    y_shape = tf.shape(y)  # [2 3]
    z_shape = tf.shape(z)  # <tf.Tensor 'Shape_5:0' shape=(3,) dtype=int32>

    print(sess.run(x_shape))  # 结果:[2 3]
    print(sess.run(y_shape))  # 结果:[2 3]
    print(sess.run(z_shape))  # 结果:[2 3 4]

    x_get_shape = x.get_shape()  # sess.run(x_get_shape)报错，返回的是TensorShape([Dimension(2), Dimension(3)]),不是tensor 或string,而是元组,不能使用 sess.run()
    x_get_shape_as_list = x.get_shape().as_list()  # 可以使用 as_list()得到具体的尺寸，x_shape=[2 3]
    # y_get_shape = y.get_shape()  # AttributeError: 'list' object has no attribute 'get_shape'
    # z_get_shape = z.get_shape()

    print(x_get_shape)  # 结果:(2, 3)
    print(x_get_shape_as_list) # 结果:[2 3]
```



#### tf.reshape

`tf.reshape(tensor, shape, name=None)`

给定 `tensor`, 返回 一个与指定`shape` 相同形状且内容与原tensor一致的新tensor.

如果 `shape` 被指定为`[-1]`,  `tensor` 就被平铺为1维的

For example:

```
# tensor 't' is [1, 2, 3, 4, 5, 6, 7, 8, 9]
# tensor 't' has shape [9]
reshape(t, [3, 3]) ==> [[1, 2, 3]
                        [4, 5, 6]
                        [7, 8, 9]]

# tensor 't' is [[[1, 1], [2, 2]]
#                [[3, 3], [4, 4]]]
# tensor 't' has shape [2,2, 2]
reshape(t, [2, 4]) ==> [[1, 1, 2, 2]
                        [3, 3, 4, 4]]

# tensor 't' is [[[1, 1, 1],
#                 [2, 2, 2]],
#                [[3, 3, 3],
#                 [4, 4, 4]],
#                [[5, 5, 5],
#                 [6, 6, 6]]]
# tensor 't' has shape [3, 2, 3]
# pass '[-1]' to flatten 't'
reshape(t, [-1]) ==> [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
```
#### tf.expand_dims

```
tf.expand_dims(input, axis=None, name=None, dim=None)
```

在第axis位置增加一个维度

给定张量输入，此操作在输入形状的维度索引轴处插入1的尺寸。 尺寸索引轴从零开始; 如果您指定轴的负数，则从最后向后计数。

如果要将批量维度添加到单个元素，则此操作非常有用。 例如，如果您有一个单一的形状[height，width，channels]，您可以使用expand_dims（image，0）使其成为1个图像，这将使形状[1，高度，宽度，通道]。

```python
# 't' is a tensor of shape [2]
shape(expand_dims(t, 0)) ==> [1, 2]
shape(expand_dims(t, 1)) ==> [2, 1]
shape(expand_dims(t, -1)) ==> [2, 1]
# 't2' is a tensor of shape [2, 3, 5]
shape(expand_dims(t2, 0)) ==> [1, 2, 3, 5]
shape(expand_dims(t2, 2)) ==> [2, 3, 1, 5]
shape(expand_dims(t2, 3)) ==> [2, 3, 5, 1]
```

#### tf.squeeze

```
tf.squeeze(input, squeeze_dims=None, name=None)
```

Removes dimensions of size 1 from the shape of a tensor. 
从tensor中删除所有大小是1的维度

给定张量输入，此操作返回相同类型的张量，并删除所有尺寸为1的尺寸。 如果不想删除所有尺寸1尺寸，可以通过指定squeeze_dims来删除特定尺寸1尺寸。
如果不想删除所有大小是1的维度，可以通过squeeze_dims指定。

For example:

```python
# 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
shape(squeeze(t)) ==> [2, 3]
Or, to remove specific size 1 dimensions:

# 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
shape(squeeze(t, [2, 4])) ==> [1, 2, 3, 1]
```

将维度为1的挤掉，如果挤掉了还是1维，就循环挤掉

```python
x=tf.constant([[1],[1],[1],[2]],name='v1')
y=tf.constant([[[123]]],name='v2')
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    print(sess.run(tf.shape(x)))
    print(sess.run(tf.squeeze(x)))
    print(sess.run(tf.shape(y)))
    print(sess.run(tf.squeeze(y)))
    
shape :  [4 1]    # 因为[[1],...]中的1在第二维度的维度为1，因此被挤掉，提了出来
result : [1 1 1 2]

shape : [1 1 1]   # 因为[[[123]]],挤出一次为 [[123]] ,再挤出为[123],再挤出为123
result : 123
```



### 矩阵操作切片与连接

#### tf.concat
```
tf.concat(values, axis, name='concat')
```

将tensor的某一维（concat_dim）的数据连接为起来，

```
t1 = [[1, 2, 3], [4, 5, 6]]
t2 = [[7, 8, 9], [10, 11, 12]]
tf.concat(0, [t1, t2]) ==> [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
tf.concat(1, [t1, t2]) ==> [[1, 2, 3, 7, 8, 9], [4, 5, 6, 10, 11, 12]]
```


values[i].shape = [D0, D1, ... Dconcat_dim(i), ...Dn]

连接结果为：

[D0, D1, ... Rconcat_dim, ...Dn] ，Rconcat_dim = sum(Dconcat_dim(i))

```
# tensor t3 with shape [2, 3]
# tensor t4 with shape [2, 3]
tf.shape(tf.concat(0, [t3, t4])) ==> [4, 3]
tf.shape(tf.concat(1, [t3, t4])) ==> [2, 6]
```
#### tf.tile矩阵复制

应用于需要张量扩展的场景，具体说来就是： 
如果现有一个形状如[`width`, `height`]的张量，需要得到一个基于原张量的，形状如[`batch_size`,`width`,`height`]的张量，其中每一个batch的内容都和原张量一模一样。`tf.tile`使用方法如： `tf.tile(input, multiples, name=None)`

```
tile(
    input,
    multiples,
    name=None
)
```

其中输出将会重复input输入multiples次。例子如：

```
import tensorflow as tf

raw = tf.Variable(tf.random_normal(shape=(1, 3, 2)))
multi = tf.tile(raw, multiples=[2, 1, 1])

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(raw.eval())
    print('-----------------------------')
    print(sess.run(multi))
```

输出如：

```
[[[-0.50027871 -0.48475555]
  [-0.52617502 -0.2396145 ]
  [ 1.74173343 -0.20627949]]]
-----------------------------
[[[-0.50027871 -0.48475555]
  [-0.52617502 -0.2396145 ]
  [ 1.74173343 -0.20627949]]

 [[-0.50027871 -0.48475555]
  [-0.52617502 -0.2396145 ]
  [ 1.74173343 -0.20627949]]]
```

可见，multi重复了raw的0 axes两次，1和2 axes不变

#### tf.slice切取tensor中指定的部分数据

函数原型 `tf.slice(inputs,begin,size,name='')`

用途：从inputs中**抽取部分内容**

- inputs：可以是list,array,tensor
- begin：n维列表(**与inputs的shape相关**，array就是2维，tensor就是3维度)，begin[i] 表示从inputs中第i维抽取数据时，相对0的起始偏移量
- size：n维列表(与inputs的shape相关，array就是2维，tensor就是3维度)，size[i]表示要抽取的第i维元素的数目

begin与size**这两个数组应该联合起来阅读**：

```python
begin_y=[1,0,0]
size_y=[1,2,3]
# 表示这个数据是tensor，有3个维度
第1列中的begin=1表示从第1个维度里的第2条数据开始,size=1表示抽取1个该维度的数据
第2列中的begin=0表示从第2个维度里的第1条数据开始,size=2表示抽取2个该维度的数据
第3列中的begin=0表示从第3个维度里的第1条数据开始,size=3表示抽取3个该维度的数据
```



```python
import tensorflow as tf
import numpy as np
x=[[1,2,3],[4,5,6]]
y=np.arange(24).reshape([2,3,4])
#y=[[[ 0  1  2  3]
#    [ 4  5  6  7]
#    [ 8  9 10 11]]
#   [[12 13 14 15]
#    [16 17 18 19]
#    [20 21 22 23]]]
z=tf.constant([[[1,2,3],[4,5,6]], [[7,8,9],[10,11,12]],  [[13,14,15],[16,17,18]]]
sess=tf.Session()
begin_x=[1,0]   # 第一个1，决定了从x的第二行[4,5,6]开始，第二个0，决定了从[4,5,6] 中的4开始抽取
size_x=[1,2]    # 第一个1决定了从第二行以起始位置抽取1行，也就是只抽取[4,5,6] 这一行，第2个2表示在这一行中从4开始抽取2个元素
out=tf.slice(x,begin_x,size_x)
print sess.run(out)  #  结果:[[4 5]]

begin_y=[1,0,0]
size_y=[1,2,3]
out=tf.slice(y,begin_y,size_y)   
print sess.run(out)  # 结果:[[[12 13 14] [16 17 18]]]
 
begin_z=[0,1,1]
size_z=[-1,1,2] 
out=tf.slice(z,begin_z,size_z)
print sess.run(out)  # size[i]=-1 表示第i维从begin[i]剩余的元素都要被抽取，结果：[[[ 5  6]] [[11 12]] [[17 18]]]
```





### GPU

#### 指定GPU

通过`nvidia-smi`查看GPU使用情况

方法1：**通过CUDA_VISIBLE_DEVICES来指定**

```python
import os
os.environ['CUDA_VISIBLE_DEVICES']='2'
```

除第2块以外的GPU全部屏蔽了，只有第2块GPU对当前运行的程序是可见的。



方法2：**通过tf.device()函数**

```
tf.device('/gpu:2')
```

虽然指定了第2块GPU来训练，但是其它几个GPU也还是被占用，只是模型训练的时候，是在第2块GPU上进行



### 其他

#### tf.argmax

`tf.argmax(input, axis, name=None)`

返回input中最大值的下标 ，是一个tensor类型of type `int64`.

- **input**: A `Tensor`.  types: `float32`, `float64`, `int64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `qint8`, `quint8`, `qint32`.
- **axis**：0 表示按列，1 表示按行


tf.argmax(vector, 1)：返回的是vector中的最大值的索引号，如果vector是一个向量，那就返回一个值，如果是一个矩阵，那就返回一个向量，这个向量的每一个维度都是相对应矩阵行的最大值元素的索引号。

```
import tensorflow as tf
import numpy as np

A = [[1,3,4,5,6]]
B = [[1,3,4], [2,4,1]]

with tf.Session() as sess:
	print(sess.run(tf.argmax(A, 1)))
	print(sess.run(tf.argmax(B, 1)))
```

输出：

```
[4]  # 6
[2 1] # 1,3,4中的4,  2,4,1中的4
```



#### tf.clip_by_value

```
tf.clip_by_value(
    t,  		#A Tensor
    clip_value_min,
    clip_value_max,
    name=None
)
```

保证tensor中值都在[clip_value_min, clip_value_max]之内，小于min的会被置为min，同理max



#### 打印tensor内容

tensor详细数值 不能直接print打印：

```
import tensorflow as tf
x = tf.constant(1)
print x

输出：
Tensor("Const:0", shape=(), dtype=int32)
```

原因： 因为我们在建立graph的时候，只建立 tensor 的 结构形状信息 ，并没有执行数据的操作。要打印输出tensor的值，需要借助 `tf.Session`，`tf.InteractiveSession`。

法一：

```
import tensorflow as tf
x = tf.constant(1)
with tf.Session() as sess:
    print(sess.run(x))
输出：1
```

法二：

```
import tensorflow as tf
x = tf.constant(1)
sess = tf.InteractiveSession()
print(x.eval())
输出：1
```
#### 



### TensoBoard

首先使用tf.summary记录要显示的变量

```
# 在模型中，添加要记录的数据
mean = tf.reduce_mean(var)# var是数组
tf.summary.scalar('mean', mean)
tf.summary.histogram('histogram', var)
merged = tf.summary.merge_all()

# 在喂数据给sess.run之前，定义writer
train_writer = tf.summary.FileWriter('log/train', sess.graph)
test_writer = tf.summary.FileWriter('log/test')

#在每batch之后，调用writer保存
summary, acc = sess.run([merged, accuracy], feed_dict={x: test_x_minmax, y_: test_y_data_trans})
train_writer.add_summary(summary, step)
```

- `Summary`：所有需要在TensorBoard上展示的统计结果。
- `tf.name_scope()`：为Graph中的Tensor添加层级，TensorBoard会按照代码指定的层级进行展示，初始状态下只绘制最高层级的效果，点击后可展开层级看到下一层的细节。
- `tf.summary.scalar()`：添加标量统计结果。
- `tf.summary.histogram()`：添加任意shape的Tensor，统计这个Tensor的取值分布。
- `tf.summary.merge_all()`：添加一个操作，代表执行所有summary操作，这样可以避免人工执行每一个summary op。
- `tf.summary.FileWrite`：用于将Summary写入磁盘，需要制定存储路径logdir，如果传递了Graph对象，则在Graph Visualization会显示Tensor Shape Information。执行summary op后，将返回结果传递给`add_summary()`方法即可。

然后可以在命令行（cmd）中执行以下命令：

```
tensorboard --logdir="path/to/log"
```

会得到一个浏览器地址，复制到浏览器打开即可



Tensorboard的可   视化过程

（1）首先肯定是先建立一个graph,你想从这个graph中获取某些数据的信息

（2）确定要在graph中的哪些节点放置summary operations以记录信息 
使用tf.summary.scalar记录标量 
使用tf.summary.histogram记录数据的直方图 
使用tf.summary.distribution记录数据的分布图 
使用tf.summary.image记录图像数据 
….

（3）operations并不会去真的执行计算，除非你告诉他们需要去run,或者它被其他的需要run的operation所依赖。而我们上一步创建的这些summary operations其实并不被其他节点依赖，因此，我们需要特地去运行所有的summary节点。但是呢，一份程序下来可能有超多这样的summary 节点，要手动一个一个去启动自然是及其繁琐的，因此我们可以使用tf.summary.merge_all去将所有summary节点合并成一个节点，只要运行这个节点，就能产生所有我们之前设置的summary data。

（4）使用tf.summary.FileWriter将运行后输出的数据都保存到本地磁盘中

（5）运行整个程序，并在命令行输入运行tensorboard的指令，之后打开web端可查看可视化的结果



### tf.contrib.layers.fully_connected

全连接层，对最后一个维度进行全连接操作

`[batch_size,seq_len,hidden_size]——>[batch_size,seq_len,num_outputs]`

```python
import tensorflow as tf
import numpy as np

input = [
    [
        [1, 2, 3, 4, ],
        [5, 6, 7, 8, ],
    ], [
        [1, 2, 3, 4, ],
        [5, 6, 7, 8, ],
    ]
]
# shape=[batch_size,seq_len,hidden_size]=[2,2,3]
input = np.array(input, dtype=np.float32)
input = tf.Variable(input)

output = tf.contrib.layers.fully_connected(input, num_outputs=2)
# shape=[batch_size,seq_len,num_outputs]=[2,2,2]
print(output.get_shape())

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    print(output.get_shape())
```