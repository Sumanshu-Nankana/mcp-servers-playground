from fastmcp import FastMCP
from fastmcp.utilities.types import Image
import pyautogui
import io

mcp = FastMCP(name="Screenshot")


@mcp.tool
def capture_screenshot() -> Image:
    """
    Capture the current screen and return the Image. Use this tool whenever the user
    requests a screenshot of their activity.
    """
    buffer = io.BytesIO()  # create an empty in-memory "file"
    screenshot = pyautogui.screenshot()
    screenshot.save(buffer, format="png")  ## write PNG bytes into it (not disk)
    return Image(
        data=buffer.getvalue(), format="png"
    )  # .getvalue() -  read all those bytes back out


if __name__ == "__main__":
    mcp.run()
