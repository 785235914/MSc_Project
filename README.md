# Msc_Project
Msc Project - Deep Transfer Learning with LSTM and CNN for EEG signals in diagnosing Schizophrenia patients

Introduction: This project aims to develop a model for EEG patients data using deep transfer learning with LSTM and CNN.

1. This section only provides code based on the MobileNet model, which is the best performance in Msc project. For other models compared in the study, it is necessary to modify the file path and code replacement of the model part according to the difference between the model and the original data segmentation.
2. The code version is provided by Colab and Py. The Colab version cannot achieve the best performance in research due to computing resources and other issues. It is mainly used to display code processes and visualize some calculation results. The model code for optimal performance this time is obtained by running in the local IDE. Whether it is ultimately achieved depends on the performance of the computer. This research uses the MacBook Pro 2021 (memory 16G), the chip is Apple M1 Pro, and the IDE is PyCharm
3. When running py files locally, you need to install machine learning, deep learning and basic computing toolkits. For example, NumPy, Pandas, Matplotlib, Seaborn, SciPy, Scikit-learn, Keras, TensorFlow, etc.
4. The image data obtained after data preprocessing needs to be saved in a folder. Due to the large amount of data, it cannot be uploaded. You need to handle and replace the file read path to ensure the model runs properly by yourself (Run the code of Data preprocessing). window_size = 25 represents data divided by 25s, and 30 represents data divided by 30s. In addition, some codes that save files locally also need comments or modifications.
5. The complete codes of different models can be obtained on GitHub. Below are links to Colab, GitHub, Orignal Data. The implementation of the model also refers to official documents such as Scikit-learn, Keras, TensorFlow, and Python.

Please check the ReadMe file to get more information
