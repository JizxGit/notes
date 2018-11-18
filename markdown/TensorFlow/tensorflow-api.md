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