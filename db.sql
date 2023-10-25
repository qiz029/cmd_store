CREATE TABLE `commands` ( `ID` INT NOT NULL AUTO_INCREMENT, `CommandBody` VARCHAR(255), `StartTime` DATETIME NOT NULL, `TimeElapsedInSec` INT NOT NULL, `ExitCode` INT NOT NULL, KEY `ExitCodeIndex` (`ExitCode`) USING BTREE, PRIMARY KEY (`ID`) );