import os
SRC_PATH = os.path.abspath(os.path.dirname(__file__))

#paths
calculated_cfg = "/Analysis/CFG"
fp_samples_train_path = "../Samples/FP_train_Samples" + calculated_cfg
fp_samples_test_path = "../Samples/FP_test_Samples" + calculated_cfg
fp_samples_validate_path = "../Samples/FP_validate_Samples" + calculated_cfg

Non_fp_samples_train_path = "../Samples/Non_FP_train_Samples" + calculated_cfg
Non_fp_samples_test_path = "../Samples/Non_FP_test_Samples" + calculated_cfg
Non_fp_samples_validate_path = "../Samples/Non_FP_validate_Samples" + calculated_cfg

Base_Fp_Test_Path = "../BasePaper/BaseTestFP" + calculated_cfg
Base_NonFp_Test_Path = "../BasePaper/BaseTestNonFp" + calculated_cfg

TrainArray = [fp_samples_train_path, Non_fp_samples_train_path]
ValidateArray = [fp_samples_validate_path,Non_fp_samples_validate_path]
# TestArray = [fp_samples_test_path,Non_fp_samples_test_path]

TestArray = [Base_Fp_Test_Path , Base_NonFp_Test_Path] #uncomment to  check base paper dataset
#modelStoredpath

model = os.path.join(SRC_PATH,"..","Analysis");
algo = "rf";
ngramssize = 5;
rftreesize = 700;
threshhold = 0.5;
ChromeAPIflag = 1
ChromePath = os.path.join(SRC_PATH,"..","temp","Analysis","CFG" );
