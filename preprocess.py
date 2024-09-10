import gradio as gr
import webbrowser
import os
import json
import subprocess
import shutil


def get_path(data_dir):
    start_path = os.path.join("./data", data_dir)
    lbl_path = os.path.join(start_path, "esd.list")
    train_path = os.path.join(start_path, "train.list")
    val_path = os.path.join(start_path, "val.list")
    config_path = os.path.join(start_path, "configs", "config.json")
    return start_path, lbl_path, train_path, val_path, config_path


def generate_config(data_dir, batch_size):
    assert data_dir != "", "数据集名称不能为空"
    start_path, _, train_path, val_path, config_path = get_path(data_dir)
    if os.path.isfile(config_path):
        config = json.load(open(config_path, "r", encoding="utf-8"))
    else:
        config = json.load(open("configs/config.json", "r", encoding="utf-8"))
    config["data"]["training_files"] = train_path
    config["data"]["validation_files"] = val_path
    config["train"]["batch_size"] = batch_size
    out_path = os.path.join(start_path, "configs")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    model_path = os.path.join(start_path, "models")
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    if not os.path.exists("config.yml"):
        shutil.copy(src="default_config.yml", dst="config.yml")
    return "配置文件生成完成"


def resample(data_dir):
    assert data_dir != "", "数据集名称不能为空"
    start_path, _, _, _, config_path = get_path(data_dir)
    in_dir = os.path.join(start_path, "raw")
    out_dir = os.path.join(start_path, "wavs")
    subprocess.run(
        [
            "python",
            "resample_legacy.py",
            "--sr",
            "44100",
            "--in_dir",
            f"{in_dir}",
            "--out_dir",
            f"{out_dir}",
        ]
    )
    return "音频文件预处理完成"


def preprocess_text(data_dir):
    assert data_dir != "", "数据集名称不能为空"
    start_path, lbl_path, train_path, val_path, config_path = get_path(data_dir)
    lines = open(lbl_path, "r", encoding="utf-8").readlines()
    with open(lbl_path, "w", encoding="utf-8") as f:
        for line in lines:
            path, spk, language, text = line.strip().split("|")
            path = os.path.join(start_path, "wavs", os.path.basename(path)).replace(
                "\\", "/"
            )
            f.writelines(f"{path}|{spk}|{language}|{text}\n")
    subprocess.run(
        [
            "python",
            "preprocess_text.py",
            "--transcription-path",
            f"{lbl_path}",
            "--train-path",
            f"{train_path}",
            "--val-path",
            f"{val_path}",
            "--config-path",
            f"{config_path}",
        ]
    )
    return "标签文件预处理完成"


def bert_gen(data_dir):
    assert data_dir != "", "数据集名称不能为空"
    _, _, _, _, config_path = get_path(data_dir)
    subprocess.run(["python", "bert_gen.py", "--config", f"{config_path}"])
    return "BERT 特征文件生成完成"


if __name__ == "__main__":
    batch_size = 24
    data_dir = "genshin"
    info = generate_config(data_dir=data_dir, batch_size=batch_size)
    print(info)
    info = resample(data_dir)
    print(info)
    info = preprocess_text(data_dir)
    print(info)
    info = bert_gen(data_dir)
    print(info)


