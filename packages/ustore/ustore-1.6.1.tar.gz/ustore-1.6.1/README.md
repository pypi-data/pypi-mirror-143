
# UStore

A simple library for the managment/usage for users

## Features

> AES encryption on config files.

> Automatic sha256 hashing on passwords with salt

> High speeds for user R/W

> Supports importing and exporting userdata

## Getting Started

### Installing

```
pip install ustore
```

### Example

```
import ustore
ustore.init(".")                                                                                     # Set user storage location to current dir
ustore.register_account("user","pass")                                    # Make a user with the username user and a password bar
ustore.setconfig("user","data","pass")                                     # Set the config value for the user user to data
ustore.getconfig("user","pass")                                                   # Get the config for the user user
ustore.valid_password("user","pass2")                                    # Check if the user user's password is pass

ustore.export_user_data()                                                             # Will export the userdata to the folder containing userdata.
ustore.import_user_data("export.uude", merge=False)  # Imports the userdata export. Without merging, deleting the current userdata folder
```

### Documentation

#### ustore.init(location-for-data-storage) 
> Will Initialise the user system to location-for-data-storage


#### register_account(username,password)
> Create an account.


#### valid_password(username,password)
> Validates if the supplied password is valid for the account.
> Returns Bool value


#### setconfig(username,configvar,password)
> Will set the config file for the user to configvar, Password must be supplied due to config file encryption


#### export_user_data()
> Will export userdata to the folder containing the userdata folder as "export.uude"


#### import_user_data(path,merge)
> Will import userdata from the specified path. Default path is the folder containing the userdata folder as "export.uude".
> If merge set true (Default) than the userdata import and current will be merged. Else the userdata folder is wiped


#### Initialisation_Error 
> Will be thrown if init() is not called


#### Invalid_Input_Error
> Will be thrown if an illegal username/password was supplied


#### User_Exists_Error
> Will be thrown if a user was trying to register an already registered user


#### Invalid_Password_Error
> Will be thrown if the password validation failed unless called by valid_password()


### Donate

#### Etheriuem address: 0x25916caa0dB559bC7F21850cfE678dc9f273A8D7

#### Nano address : nano_1is4sj8jg1uzmtzhowr7iycn17r99y9xotr73w944gdicqozxk6c9ay14yqs