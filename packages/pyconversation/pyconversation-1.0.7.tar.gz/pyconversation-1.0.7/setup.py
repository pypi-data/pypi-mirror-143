import setuptools
import pathlib

current_dir = pathlib.Path(__file__).parent

with open(current_dir / "README.md", "r") as readme:
	readme_text = readme.read()

setuptools.setup(
	name="pyconversation",
	version="1.0.7",
	author="Roman Melamud",
	description="Zero-dependency library for chat-bot creators with deadlines. It allows you to describe a conversation, talk with user according to your schema and restore it, if something went wrong.",
	long_description=readme_text,
	long_description_content_type="text/markdown",
	license="MIT",
	packages=setuptools.find_packages(current_dir),
	classifiers=[
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
	],
	python_requires=">=3.6",
	py_modules=["util_types", "loggers", "messages", "sender"],
	package_dir={"": "."},
	install_requires=[],
	url="https://github.com/R-Mielamud/py-conversation.git",
	project_urls = {
        "Bugs": "https://github.com/R-Mielamud/py-conversation/issues",
		"Homepage": "https://github.com/R-Mielamud/py-conversation#readme",
    },
)
