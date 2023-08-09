# Imagine you have a list of strings, where each string represents a version number in the format "x.y.z" (e.g., "1.2.3").
# Implement a function that sorts the list of version numbers in ascending order.
#
# Rules:
#
# - Each version number is a string consisting of three non-negative integers separated by periods.
# - You can assume that each version number has exactly three parts, and each part is an integer.
# - The sorting should be done based on the following priority: major version > minor version > patch version.
# - You are not allowed to use any built-in sorting functions or libraries.
#
# Example:
#
# Input: ["1.0.0", "0.5.7", "0.5.6", "1.1.0", "1.0.1"]
# Output: ["0.5.6", "0.5.7", "1.0.0", "1.0.1", "1.1.0"]
#
# ----------------------------------------------------------------------------


def sort_versions(versions_list: list):
    numbers_list = [
        float(remove_point_at_position(version, 2)) for version in versions_list
    ]

    for index1 in range(0, len(numbers_list)):
        min_number = numbers_list[index1]
        min_version = versions_list[index1]
        for index2 in range(index1, len(numbers_list)):
            if numbers_list[index2] < min_number:
                temp_number = min_number
                temp_version = min_version
                min_number = numbers_list[index2]
                min_version = versions_list[index2]
                numbers_list[index2] = temp_number
                versions_list[index2] = temp_version
            if numbers_list[index2] == min_number:
                if versions_list[index2].replace(".", "", 1) < min_version.replace(
                    ".", "", 1
                ):
                    temp_number = min_number
                    temp_version = min_version
                    min_number = numbers_list[index2]
                    min_version = versions_list[index2]
                    numbers_list[index2] = temp_number
                    versions_list[index2] = temp_version
        numbers_list[index1] = min_number
        versions_list[index1] = min_version
    return versions_list


def remove_point_at_position(version: str, pos: int):
    count = 0
    for i in range(len(version)):
        if version[i] == ".":
            count += 1
            if count == pos:
                return version[:i] + version[i + 1 :]


# Example usage:
input_versions = [
    "1.0.0",
    "0.5.7",
    "0.5.6",
    "1.1.0",
    "1.0.1",
    "11.1.1",
    "1.11.1",
    "1.1.11",
    "11.11.11",
    "1.11.11",
    "11.11.1",
    "11.1.11",
]

sorted_versions = sort_versions(input_versions)
print(f"Sorted version numbers: {sorted_versions}")
