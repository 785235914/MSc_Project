from tensorflow import image
import keras
print(keras.__version__)
from keras.preprocessing import image
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from keras.wrappers.scikit_learn import KerasClassifier
import os
import torchvision.models as models
ResNet50 = models.resnet50(pretrained=True)
import cv2
from keras.layers import Reshape
from keras.optimizers import Adam, RMSprop, SGD
from skopt import BayesSearchCV
from keras.layers import LSTM, Dense, Flatten
from keras.models import Model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
from keras.applications import DenseNet121,DenseNet169,DenseNet201
from keras.applications import InceptionV3
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.xception import Xception
from keras.applications.nasnet import NASNetLarge, NASNetMobile
from keras.applications import ResNet50,ResNet101,ResNet152
from keras.applications import MobileNet,MobileNetV2,MobileNetV3Small,MobileNetV3Large
from keras.applications import VGG16,VGG19
import time
from keras.layers import Reshape
from keras.optimizers import Adam, RMSprop, SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import regularizers
from keras.callbacks import ReduceLROnPlateau
from keras.layers import BatchNormalization
import numpy as np
import tensorflow as tf

np.random.seed(42)
tf.random.set_seed(42)

# 指定文件夹路径
# 指定文件夹路径
healthy_save_path = '/Users/yuanyi/学习/毕业论文/毕业论文题目/Pycharm_Code/healthy30'
schizophrenia_save_path = '/Users/yuanyi/学习/毕业论文/毕业论文题目/Pycharm_Code/schizophrenia30'

# 假设你已经完成了小波时频图的生成并保存在本地文件夹中
# 定义“healthy”和“schizophrenia”文件夹路径
healthy_folder = healthy_save_path
schizophrenia_folder = schizophrenia_save_path

def load_images(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img_path = os.path.join(folder, filename)
            # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # 以灰度模式读取图片
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)  # 以RGB模式读取图片
            img_resized = cv2.resize(img, (224, 224))  # 调整图像大小到64x64
            img_array = img_resized / 255.0  # 将像素值归一化到[0, 1]
            images.append(img_array)
            labels.append(0 if folder == healthy_folder else 1)
    return np.array(images), np.array(labels)

# 加载和处理图像
X_healthy, y_healthy = load_images(healthy_folder)
X_schizophrenia, y_schizophrenia = load_images(schizophrenia_folder)

# 将数据集合并
X = np.concatenate((X_healthy, X_schizophrenia), axis=0)
y = np.concatenate((y_healthy, y_schizophrenia), axis=0)

# 打乱数据集
indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
y = y[indices]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# 原始数据集的形状
# input_shape = (256, 256, 3)
input_shape = (224, 224, 3)
# input_shape = (128, 128, 3)


def create_model(optimizer='adam',activation='sigmoid',units=128, dropout=0.2,
                 recurrent_dropout=0.2,learning_rate=0.001,epochs=100, batch_size=64):
    # 加载预训练的MobileNet模型
    base_model = DenseNet169(weights='imagenet', include_top=False, input_shape=input_shape)
    # 设定不更新预训练模型的权重
    for layer in base_model.layers:
        layer.trainable = False

    # 获取base_model的输出，然后添加新的层
    base_model_output = base_model.output

    # 获取模型最后一层的输出形状
    output_shape = base_model.output_shape
    print('Output Shape: ', output_shape)

    # 输出形状是一个形状元组，其形式为 (None, height, width, depth)
    # 其中 height, width, depth 是特征图的高度，宽度和深度（也就是特征的数量）
    # 这里我们只关心深度，因为它是我们要传入 LSTM 的特征数量

    features_dim = output_shape[-1]  # 提取深度维度
    print('Features Dimension: ', features_dim)

    # 添加Reshape层
    # 我们可以使用从 base_model 获取的 features_dim 来重新塑造特征
    x = Reshape((-1, features_dim))(base_model_output)
    print('Reshape : ', x)

    # 添加LSTM层
    x = LSTM(units, dropout=dropout, recurrent_dropout=recurrent_dropout)(x)
    # 批量归一化 (Batch Normalization): 在模型中添加批量归一化层可以帮助改善训练速度和模型的性能。
    # x = BatchNormalization()(x)
    x = Dense(1, activation='sigmoid')(x)

    # 构建最终模型
    model = Model(inputs=base_model.input, outputs=x)

    if optimizer == 'adam':
        optimizer = Adam(learning_rate=learning_rate)
    elif optimizer == 'rmsprop':
        optimizer = RMSprop(learning_rate=learning_rate)
    elif optimizer == 'sgd':
        optimizer = SGD(learning_rate=learning_rate)

    # 编译模型
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    # 训练模型
    # # 注意：这可能需要较大的计算资源（例如，GPU）
    # model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size)

    # 创建早停回调
    # early_stopping = EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)

    # 创建模型检查点回调
    # model_checkpoint = ModelCheckpoint('Model/MobileNet_Random_Best_Model.h5', monitor='val_loss', save_best_only=True)

    # 在模型训练过程中添加这两个回调
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size)
    # model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, callbacks=[early_stopping])
    # model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, callbacks=[early_stopping, model_checkpoint])

    return model


lstm_best_params = {'units': 128,
                     'recurrent_dropout': 0.2,
                     'optimizer': 'rmsprop',
                     'learning_rate': 0.001,
                     'epochs': 50,
                     'dropout': 0.2,
                     'batch_size': 64,
                     'activation': 'sigmoid'
                     }

from sklearn.metrics import roc_auc_score, f1_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

from keras.models import load_model

# 从本地文件加载模型 # 用你保存的模型文件路径替换这里的路径
# lstm_best_params = load_model('/Users/yuanyi/学习/毕业论文/毕业论文题目/Pycharm_Code/TestModel/224-MobieNet-Random-Model-0811.h5')
# best_model = load_model('/Users/yuanyi/学习/毕业论文/毕业论文题目/Pycharm_Code/Model/224-MobileNetV2-LSTM_Best_Model.h5')
#
# lstm_best_params = random_best_model.best_params_

# 使用最佳参数创建LSTM模型
lstm_best_model = create_model(optimizer=lstm_best_params['optimizer'],
                               activation=lstm_best_params['activation'],
                               units=lstm_best_params['units'],
                               dropout=lstm_best_params['dropout'],
                               recurrent_dropout=lstm_best_params['recurrent_dropout'],
                               learning_rate=lstm_best_params['learning_rate'],
                               epochs=lstm_best_params['epochs'],
                               batch_size=lstm_best_params['batch_size'])
# 训练模型
lstm_best_model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=lstm_best_params['epochs'], batch_size=lstm_best_params['batch_size'], verbose=1)

# 获取训练集上的损失和精确度
train_loss, train_accuracy = lstm_best_model.evaluate(X_train, y_train, batch_size=lstm_best_params['batch_size'])

# 获取验证集上的损失和精确度
val_loss, val_accuracy = lstm_best_model.evaluate(X_test, y_test, batch_size=lstm_best_params['batch_size'])
lstm_best_model.save('LabTestModel30s/DenseNet169-30s-LSTM_Best_Model(224-25s).h5')


print("Train Loss: ", train_loss)
print("Train Accuracy: ", train_accuracy)
print("Validation Loss: ", val_loss)
print("Validation Accuracy: ", val_accuracy)


best_model= lstm_best_model
# # 在测试集上评估模型
# train_loss, train_accuracy = best_model.evaluate(X_train, y_train,batch_size=128)
# val_loss, val_accuracy = best_model.evaluate(X_test, y_test,batch_size=128)
#
# print("Train Loss: ", train_loss)
# print("Train Accuracy: ", train_accuracy)
# print("Validation Loss: ", val_loss)
# print("Validation Accuracy: ", val_accuracy)

from sklearn.metrics import roc_auc_score, f1_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
# 使用模型进行预测
y_pred = best_model.predict(X_test)
y_train_pred = best_model.predict(X_train)

# 计算ROC曲线的各个点
fpr, tpr, _ = roc_curve(y_test, y_pred)
fpr_train, tpr_train, _ = roc_curve(y_train, y_train_pred)

# 计算AUC
roc_auc = auc(fpr, tpr)
roc_auc_train = auc(fpr_train, tpr_train)

# 绘制ROC曲线
plt.figure()
plt.plot(fpr, tpr, color='darkorange', label='Test ROC Curve (area = %0.2f)' % roc_auc)
plt.plot(fpr_train, tpr_train, color='red', label='Train ROC Curve (area = %0.2f)' % roc_auc_train)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('DenseNet169 - Receiver Operating Characteristic')
plt.legend(loc="lower right")

save_path = '/Users/yuanyi/学习/毕业论文/毕业论文题目/Pycharm_Code/LabTestModel30s'
# 保存图像
plt.savefig(f'{save_path}/DenseNet169-30s - Receiver Operating Characteristic.png')

plt.show()


from sklearn.metrics import precision_recall_curve, auc
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

# 假设 y_test 是测试集的真实标签，y_scores 是模型的预测分数

# 精确度-召回率曲线
precision, recall, _ = precision_recall_curve(y_test, y_pred)
plt.figure()
plt.plot(recall, precision, label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('DenseNet169 - Precision-Recall curve')
plt.legend(loc="lower left")

# 保存图像
plt.savefig(f'{save_path}/DenseNet169-30s - Precision-Recall curve.png')

plt.show()


# 将预测结果二值化，即将预测结果转换为0或1
y_pred = np.where(y_pred > 0.5, 1, 0)
# print("y_pred: ", y_pred)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)

# 计算F1得分
f1 = f1_score(y_test, y_pred)

# 计算AUC得分
auc = roc_auc_score(y_test, y_pred)

# 计算精度
precision = precision_score(y_test, y_pred)

# 计算召回率
recall = recall_score(y_test, y_pred)

print("Accuracy: ", accuracy)
print("F1 Score: ", f1)
print("AUC: ", auc)
print("Precision: ", precision)
print("Recall: ", recall)

print("Train Accuracy: ", train_accuracy)
print("Validation Accuracy: ", val_accuracy)


# DenseNet169-30s
# Accuracy:  0.8671328671328671
# F1 Score:  0.8758169934640523
# AUC:  0.8664799253034547
# Precision:  0.8758169934640523
# Recall:  0.8758169934640523
# Train Accuracy:  1.0
# Validation Accuracy:  0.867132842540741