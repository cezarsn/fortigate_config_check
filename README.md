The software is created in order to be able to check diffrent Fortigate configurations (version 4 and 5).
Because the Fortigate configs are not consistent in version 4 this first implementation is intended for version 5 and will be updated with the features to parse also version 4.
The software is based on the config parser developed at http://jmanteau.fr/informatique/python/parsing-fortigate-configuration-in-python/ and this work just for version 5.0.
For version 4.0 you need to adjust your configuration file in order to avoid sections like: 

config vdom
edit root
end

where "edit" does not have a closing "next"
In order to make it work with version 4.0 you should update the config and include the next like this:

config vdom
	edit root
	next
end

or to delete the section.


Features to be build in:

-Move the file read function to the main() method.
-Check for the same configuration settings in diffrent files.
-Security check should take care of the default version of a setting even if the setting is not specified in the config.
-Abstact the Fortigate_Check class in order to provide a security list  that should be processed by the Fortigate_Check class