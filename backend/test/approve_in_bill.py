# -*- coding: UTF-8 -*-
"""
@Project : mespy
@File    : approve_in_bill.py
@Author  : guhua@jiqid.com
@Date    : 2025/09/24 15:15
"""
import requests
import json


def test_approve_in_bill():
    """测试入库单审核接口"""

    # 接口配置
    url = "http://mes.jiqid.net/api/v1/mes/dy/pallet/approve_in_bill"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    # 请求数据
    data = {
        "items": [
            {
                "pallet_pid": "31834",
                "pallet_key": "PQBH4210CN58A000088ALN",
                "k3orderkey_s": "SO2024001",
                "k3orderkey": "K320240001"
            },
            {
                "pallet_pid": "31833",
                "pallet_key": "PQBH4209CN58A000046ALN",
                "k3orderkey_s": "SO2024001",
                "k3orderkey": "K320240001"
            }
        ]
    }

    try:
        # 发送请求
        response = requests.post(url, headers=headers, json=data, timeout=300)

        # 输出结果
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")

        # 尝试解析JSON
        if response.text:
            try:
                result = response.json()
                print(f"JSON解析结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print("响应不是有效的JSON格式")

        # 检查请求是否成功
        if response.status_code == 200:
            print("✅ 请求成功")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")


if __name__ == "__main__":
    test_approve_in_bill()
