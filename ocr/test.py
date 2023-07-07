# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> ocr_api20210707Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client(
            os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
        recognize_basic_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            url='https://img-bsy.515ppt.com/515ppt/00/33/54/88/335488_c8e7e428b4ad61e72c27985527830bb6.jpg!/fw/840/unsharp/true'
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            print(client.recognize_basic_with_options(
                recognize_basic_request, util_models.RuntimeOptions()))
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # @staticmethod
    # async def main_async(
    #     args: List[str],
    # ) -> None:
    #     # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
    #     # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
    #     client = Sample.create_client(
    #         os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
    #     recognize_basic_request = ocr_api_20210707_models.RecognizeBasicRequest(
    #         url='your_value'
    #     )
    #     try:
    #         # 复制代码运行请自行打印 API 的返回值
    #         await client.recognize_basic_with_options_async(recognize_basic_request, util_models.RuntimeOptions())
    #     except Exception as error:
    #         # 如有需要，请打印 error
    #         UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
