import sys;
from TreeCreation import *

def main():
    fp_samples_train_path = "../Samples/FP_train_Samples"
    fp_samples_test_path = "../Samples/FP_test_Samples"
    fp_samples_validate_path = "../Samples/FP_validate_Samples"

    Non_fp_samples_train_path = "../Samples/Non_FP_train_Samples"
    Non_fp_samples_test_path = "../Samples/Non_FP_test_Samples"
    Non_fp_samples_validate_path = "../Samples/Non_FP_validate_Samples"


    store_cfg_folder(fp_samples_train_path);
    store_cfg_folder(fp_samples_test_path);
    store_cfg_folder(fp_samples_validate_path);

    store_cfg_folder(Non_fp_samples_train_path );
    store_cfg_folder(Non_fp_samples_validate_path);
    store_cfg_folder(Non_fp_samples_test_path);


def store_cfg_folder(folder_js):
    for r, d, f in os.walk(folder_js):
        for file in f:
            createAST(os.path.join(r, file),d);

"""Comment when using chrome extension"""
# if __name__ == "__main__":
#     main();         # to create CFG of all the files of the dataset