import json
import logging
import os

from diem import testnet, chain_ids

liquidity_account_name = "liquidity"

ENV_FILE_NAME = os.getenv("ENV_FILE_NAME", ".env")


def to_compact_json(d: dict) -> str:
    return json.dumps(d, separators=(",", ":"))


if __name__ == "__main__":
    print(f"Creating {ENV_FILE_NAME} file")
    chain_id = int(os.getenv("CHAIN_ID", testnet.CHAIN_ID.value))
    json_rpc_url = os.getenv("JSON_RPC_URL", "https://testnet.diem.com/v1")

    private_keys = os.environ.get("CUSTODY_PRIVATE_KEYS")
    if private_keys is None: # there is no dd private key provided for testnet
        with open(ENV_FILE_NAME, "w") as dotenv:
            dotenv.write(f"JSON_RPC_URL={json_rpc_url}\n")
            dotenv.write(f"CHAIN_ID={chain_id}\n")
    else:
        # dd liquidity provider
        lp_custody_private_keys = to_compact_json(
            {liquidity_account_name: private_keys}
        )

        vasp_address = os.environ["LIQUIDITY_VASP_ADDR"]
        with open(ENV_FILE_NAME, "w") as dotenv:
            dotenv.write(f"LIQUIDITY_CUSTODY_ACCOUNT_NAME={liquidity_account_name}\n")
            dotenv.write(f"CUSTODY_PRIVATE_KEYS={lp_custody_private_keys}\n")
            dotenv.write(f"LIQUIDITY_VASP_ADDR={vasp_address}\n")
            dotenv.write(f"JSON_RPC_URL={json_rpc_url}\n")
            dotenv.write(f"CHAIN_ID={chain_id}\n")
