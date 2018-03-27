#source ~/tensorflow/bin/activate
import numpy as np  # Linear algebra
import pandas as pd # Data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Activation, Dropout, MaxPooling2D, Flatten, GlobalMaxPooling2D, BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import SGD, Adam
from keras.preprocessing.image import ImageDataGenerator

# Many things affect the backscatter of the ocean or background area. High winds will generate a brighter background.
# Conversely, low winds will generate a darker background.
# Generally, the ocean background will be darker at a higher incidence angle.

# (0) Load data
train = pd.read_json('./data/train.json')
test = pd.read_json('./data/test.json')

'''
################## [What are train and test?]
repeat = True
while(repeat):
	print("TRAIN ID : " + train['id']) # prints 1604 hexadecimal ID numbers
	print("TEST ID  : " + test['id']) # prints 8423 hexadecimal ID numbers
	print(train['band_1']) # prints 1604 75-by-75 matrices
	print(train['is_iceberg']) # prints out 1 or 0. Test does not have this feature.
	repeat = False
'''
# (1) Preprocess data
# These are two arrays each containing 1604 images that are stored as a 75-by-75 matrix
X_band_1=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in train["band_1"]]) # reshapes each band_1 into 75 arrays with 75 values (i.e. 75*75 matrix)
X_band_2=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in train["band_2"]])

'''
################## [What are X_band_1 and _2?]
repeat = True
while(repeat):
	print(len(X_band_1)) #1604 images
	print(len(X_band_1[0])) #75 rows
	print(len(X_band_1[0][0])) #75 values in one row
	print("===========")
	print(len(X_band_2)) #1604 images
	print(len(X_band_2[0])) #75 rows
	print(len(X_band_2[0][0])) #75 values in one row
	print(train['id'])
	repeat = False
'''

# (2) Create third channel, which is the avg of the first two channels
#X = np.concatenate([X_band_1[:, :, :, np.newaxis], X_band_2[:, :, :, np.newaxis],((X_band_1+X_band_2)/2)[:, :, :, np.newaxis]], axis=-1)
X_b1 = np.concatenate([X_band_1[:, :, :, np.newaxis], X_band_1[:, :, :, np.newaxis],((X_band_1+X_band_1)/2)[:, :, :, np.newaxis]], axis=-1)
X_b2 = np.concatenate([X_band_2[:, :, :, np.newaxis], X_band_2[:, :, :, np.newaxis],((X_band_2+X_band_2)/2)[:, :, :, np.newaxis]], axis=-1)

'''
print("X")
print(len(X_test[0][0][0]))
print(X_test[0][0][0])
print(X_test.shape) # (1604, 75, 75, 3)
print(X_test.ndim)  # 4
'''

target = train['is_iceberg']
ID = test['id']
X_band_1=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in test["band_1"]])
X_band_2=np.array([np.array(band).astype(np.float32).reshape(75, 75) for band in test["band_2"]])
#Test = np.concatenate([X_band_1[:, :, :, np.newaxis], X_band_2[:, :, :, np.newaxis],((X_band_1+X_band_2)/2)[:, :, :, np.newaxis]], axis=-1)
Test_b1 = np.concatenate([X_band_1[:, :, :, np.newaxis], X_band_1[:, :, :, np.newaxis],((X_band_1+X_band_1)/2)[:, :, :, np.newaxis]], axis=-1)
Test_b2 = np.concatenate([X_band_2[:, :, :, np.newaxis], X_band_2[:, :, :, np.newaxis],((X_band_2+X_band_2)/2)[:, :, :, np.newaxis]], axis=-1)

# (3) Split test and train
# X is generated in the step above
# Test is 25% of the training dataset, which is 401 images
# random_state is the seed used by the random number generator
x_train_b1, x_test_b1, y_train_b1, y_test_b1 = train_test_split(X_b1,target,test_size=0.25,stratify=target,random_state=10)
x_train_b2, x_test_b2, y_train_b2, y_test_b2 = train_test_split(X_b2,target,test_size=0.25,stratify=target,random_state=10)

'''
################## [What are x_train, x_test etc?]
print(len(x_train)) #1203
print(len(x_test))  #401
print(len(y_train)) #1203
print(len(y_test))  #401
'''

# Data generator by rotation
# This cancels out orientation of image as a factor in classification
datagen = ImageDataGenerator(horizontal_flip = True,
                         vertical_flip = True,
                         width_shift_range = 0.,
                         height_shift_range = 0.,
                         channel_shift_range=0,
                         zoom_range = 0.2,
                         rotation_range = 10)


# Build a simple convolutional neural net
def buildCNN(batch_size, epochs, x_train, x_test, y_train, y_test, Test, outputName):

	model = Sequential()

	# Normalize activations (apply transformation that maintains the mean activation to 0 and std diev to 1)
	model.add(BatchNormalization(input_shape=(75,75,3)))

	# First layer
	model.add(Conv2D(32, kernel_size=(3, 3),padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	# Second layer
	model.add(Conv2D(64, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	# Third layer
	model.add(Conv2D(128,kernel_size=(3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	# Fourth layer
	model.add(Conv2D(32, kernel_size=(3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	# Pooling
	model.add(GlobalMaxPooling2D())

	model.add(Dense(64)) #512
	model.add(Activation('relu'))

	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
	model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])

	check = ModelCheckpoint("weights.{epoch:02d}-{val_acc:.5f}.hdf5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=True, mode='auto')
	early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='max')

	model.fit_generator(datagen.flow(x_train, y_train, batch_size=num_batches),steps_per_epoch=len(x_train)/32,epochs=num_epochs,callbacks=[check,early],validation_data=(x_test,y_test))

	# Generate predictions
	pred = model.predict_proba(Test_b1)

	# Submit result
	submission = pd.DataFrame()
	submission['id'] = ID
	submission['is_iceberg'] = pred
	submission.to_csv(outputName, index=False)

# (I) Try different image bands
#buildCNN(x_train_b1, x_test_b1, y_train_b1, y_test_b1, Test_b1, "submissions_b1") # Best epoch: 0.7282, 0.7606
#buildCNN(num_batches, num_epochs, x_train_b2, x_test_b2, y_train_b2, y_test_b2, Test_b2, "submissions_b2") # Best epoch: 0.8279, 0.8429

# We can see that the best model is one that uses only band2. We will only use band two in the following optimizations.

# (II) Try different epochs & batch sizes
num_batches = 32
num_epochs = 12
print("\nnum_batches = %d\nnum_epochs = %d\n" % (num_batches, num_epochs))

buildCNN(num_batches, num_epochs, x_train_b2, x_test_b2, y_train_b2, y_test_b2, Test_b2, "submissions.csv") # Best epoch: 0.8404, 0.8105
