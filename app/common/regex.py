from pydantic import constr

DniStr = constr(strip_whitespace=True, regex=r"^[0-9]{8}$")
