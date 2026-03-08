from fastmcp import FastMCP
import httpx


mcp = FastMCP(name="Crypto")


@mcp.tool
def get_cryptocurrency_price(crypto: str):
    """
    Get the price of a cryptocurrency.
    Args:
        crypto: symbol of the cryptocurrency (e.g. bitcoin)
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto.lower(), "vs_currencies": "usd"}
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = data.get(crypto.lower(), {}).get("usd")

        if price is not None:
            return f"The price of {crypto} is ${price} USD"
        else:
            return f"Price for {crypto} not found"
    except Exception as e:
        return f"Error fetching price for {crypto}: {e}"


if __name__ == "__main__":
    mcp.run()
