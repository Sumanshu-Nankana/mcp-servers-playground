from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(name="register_employee")


class Person(BaseModel):
    first_name: str = Field(..., description="The person's first name")
    last_name: str = Field(..., description="The person's last name")
    years_of_experience: int = Field(..., description="Number of years of experience")
    previous_addresses: list[str] = Field(
        default_factory=list, description="List of previous addresses"
    )


@mcp.tool
def add_person_to_member_database(person: Person) -> str:
    """
    Logs the personal details of the given person to the database.
    Args:
        person (Person): An instance of the Person class containing the following fields:
          - first_name (str): The person's first name
          - last_name (str): The person's last name
          - years_of_experience (int): The number of years of experience
          - previous_addresses (list[str]): The list of persons previous addresses
    Returns:
        str: An confirmation message indicating that the data has been logged.
    """
    with open("log.txt", "a") as log_file:
        log_file.write(f"First Name: {person.first_name}\n")
        log_file.write(f"Last Name: {person.last_name}\n")
        log_file.write(f"Years of Experience: {person.years_of_experience}\n")
        log_file.write("Previous Addresses:\n")

        for idx, address in enumerate(person.previous_addresses):
            log_file.write(f"\t{idx + 1}: {address}\n")
        log_file.write("\n")

    return "Data successfully logged."


if __name__ == "__main__":
    mcp.run()
