from fastmcp import FastMCP


mcp = FastMCP(name="resources")


@mcp.resource(uri="inventory://overview")
def get_inventory_overview() -> str:
    """
    Returns overview of inventory.
    """
    overview = """
    Inventory Overview:
     - Coffee
     - Milk
     - Tea
     - Cookies
    """

    return overview


inventory_id_to_price = {"123": "699", "456": "799", "789": "899", "976": "999"}

inventory_name_to_id = {
    "Coffee": "123",
    "Milk": "456",
    "Tea": "789",
    "Cookies": "976",
}


@mcp.resource(uri="inventory://{inventory_id}/price")
def get_inventory_price_from_inventory_id(inventory_id: str) -> str:
    """
    Returns price from inventory id.
    Args:
    inventory_id (str): inventory id.
    """
    if inventory_id not in inventory_id_to_price:
        return f"Inventory ID {inventory_id} not found."

    return inventory_id_to_price[inventory_id]


@mcp.resource(uri="inventory://{inventory_name}/name")
def get_inventory_id_from_inventory_name(inventory_name: str) -> str:
    """
    Returns inventory id from inventory name.
    Args:
    inventory_name (str): inventory name.
    """
    if inventory_name not in inventory_name_to_id:
        return f"Inventory item {inventory_name} not found."
    return inventory_name_to_id[inventory_name]


if __name__ == "__main__":
    mcp.run()
