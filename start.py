# 导入库
import qcloud_cos
import os
import subprocess

# 从env中获取配置
secret_id = os.environ.get("SECRET_ID")  # 替换为env中的变量名
secret_key = os.environ.get("SECRET_KEY")  # 替换为env中的变量名
region = os.environ.get("REGION")  # 替换为env中的变量名
bucket = os.environ.get("BUCKET")  # 替换为env中的变量名

# 定义配置
config = qcloud_cos.CosConfig(
    Secret_id=secret_id,  # 使用env中的变量
    Secret_key=secret_key,  # 使用env中的变量
    Region=region,  # 使用env中的变量
)

# 创建客户端
client = qcloud_cos.CosS3Client(config)

# 定义public目录的路径
public_path = "public"

# 定义你的命令和参数
version = os.environ.get("VERSION")  # 替换为env中的变量名
command = [
    "java",
    "-jar",
    "-Xmx2048m",
    "McPatchManage-1.1.13.jar",
    "c",
    version,
    "y",
    "q",
]

# 执行你的命令，并获取退出码
p = subprocess.run(command)
exit_code = p.returncode

# 如果退出码是0，就继续上传
if exit_code == 0:
    # 遍历public目录中的所有文件
    for root, dirs, files in os.walk(public_path):
        for file in files:
            # 获取文件的本地路径
            local_path = os.path.join(root, file)
            # 获取文件的COS路径，去掉public前缀
            cos_path = file  # 直接用文件名作为Key
            # 上传文件到COS
            response = client.upload_file(
                Bucket=bucket,  # 使用env中的变量
                LocalFilePath=local_path,  # 本地文件的路径
                Key=cos_path,  # 上传到桶的路径
                EnableMD5=False,  # 是否支持MD5
            )
            # 打印上传结果
            print("Upload {} to {} success".format(local_path, cos_path))
# 如果退出码不是0，就退出程序
else:
    print("Command failed with exit code {}".format(exit_code))
    exit()
