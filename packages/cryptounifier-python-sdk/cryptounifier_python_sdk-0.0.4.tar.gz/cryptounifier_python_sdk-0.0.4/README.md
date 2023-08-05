# CryptoUnifier PYTHON SDK

A simple PYTHON SDK for interacting with [Crypto Unifier](https://cryptounifier.io) API V1.

## Installation

You can install the package via pypi:

```bash
pip install cryptounifier_python_sdk
```

## Usage

### Using the Wallet API client

You can use the `WalletAPI` class for convenient access to API methods. Some are defined in the code:

```python
from  cryptounifier_python_sdk import MerchantAPI

client = new WalletAPI("WALLET_KEY", "SECRET_KEY", "btc")

balance = client.getBalance()
print(balance)

depositAddresses = client.getDepositAddresses()
print(depositAddresses)
```

### Using the Merchant API client

You can use the `MerchantAPI` class for convenient access to API methods. Some are defined in the code:

```python
from  cryptounifier_python_sdk import MerchantAPI

client = new MerchantAPI("MERCHANT_KEY", "SECRET_KEY")

invoice = client.createInvoice(["btc", "bch", "eth"])
print(invoice)
```

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.