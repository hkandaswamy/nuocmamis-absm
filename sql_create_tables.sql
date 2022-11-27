# Create Table for Companies
CREATE TABLE `companies` (
	`companyID` int NOT NULL AUTO_INCREMENT,
	`companyName` varchar(255) COLLATE utf8_bin NOT NULL,
	`address1` varchar(255) COLLATE utf8_bin NOT NULL,
	`address2` varchar(255) COLLATE utf8_bin,
	`companyCity` varchar(255) COLLATE utf8_bin,
	`companyState` varchar(255) COLLATE utf8_bin,
	`companyZip` int NOT NULL,
	`companyCountry` varchar(255) COLLATE utf8_bin NOT NULL,
	`salesperson` varchar(255) COLLATE utf8_bin NOT NULL,
	`companyPhone` int,
	`companyPhoneExtension` int,
	`companyFax` int,
	`companyEmail` varchar(255) COLLATE utf8_bin,
	`companyWebAddress` varchar(255) COLLATE utf8_bin,
	`companyTaxID` varchar(255) COLLATE utf8_bin,
	`status` varchar(255) COLLATE utf8_bin NOT NULL,
	`creditChecked` bool NOT NULL,
	`customer` bool NOT NULL,
	`vendor` bool NOT NULL,
	`oem` bool NOT NULL,
	`otherClassification` varchar(255) COLLATE utf8_bin,
	`notes` varchar(255) COLLATE utf8_bin,
PRIMARY KEY (`companyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;

CREATE TABLE `contacts` (
	`companyID` int NOT NULL AUTO_INCREMENT,
	`companyName` varchar(255) COLLATE utf8_bin NOT NULL,
	`contactFirstName` varchar(255) COLLATE utf8_bin NOT NULL,
	`contactLastName` varchar(255) COLLATE utf8_bin,
	`function` varchar(255) COLLATE utf8_bin,
	`contactTitle` varchar(255) COLLATE utf8_bin,
	`contactDepartment` varchar(255) COLLATE utf8_bin,
	`contactAddress1` varchar(255) COLLATE utf8_bin,
	`contactAddress2` varchar(255) COLLATE utf8_bin,
	`contactCity` varchar(255) COLLATE utf8_bin,
	`contactState` varchar(255) COLLATE utf8_bin,
	`contactZip` int,
	`contactCountry` varchar(255) COLLATE utf8_bin,
	`contactPhone` int,
	`contactExtension` int,
	`contactFax` int,
	`contactEmail` varchar(255) COLLATE utf8_bin,
	`contactNotes` varchar(255) COLLATE utf8_bin,
	FOREIGN KEY `companyID` REFERENCES companies(`companyID`),
	FOREIGN KEY `companyName` REFERENCES companies(`companyName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;

CREATE TABLE `warehouses` (
	`locationID` varchar(255) COLLATE utf8_bin NOT NULL,
	`customerID` varchar(255) COLLATE utf8_bin NOT NULL,
	`absItemID` varchar(255) COLLATE utf8_bin,
	`mfrPN` varchar(255) COLLATE utf8_bin,
	`productID` varchar(255) COLLATE utf8_bin,
	`locationQuantity` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;

CREATE TABLE `products` (
    `customerID` int NOT NULL,
    `oemID` int NOT NULL AUTO_INCREMENT,
    `productType` varchar(1000) COLLATE utf8_bin NOT NULL,
    `title` varchar(1000) COLLATE utf8_bin NOT NULL,
    `productDescription` varchar(1000) COLLATE utf8_bin,
    `colorNotes` varchar(1000) COLLATE utf8_bin,
    `packagingNotes` varchar(1000) COLLATE utf8_bin,
    `productNotes` varchar(1000) COLLATE utf8_bin,
    `serviceNotes` varchar(1000) COLLATE utf8_bin,
    `insert` varchar(1000) COLLATE utf8_bin,
    PRIMARY KEY (`oemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Table for Product information'
AUTO_INCREMENT=1 ;

CREATE TABLE `customer` (
  `customerID` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `firstName` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `lastName` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8mb4_bin DEFAULT NULL,
  `billingAddress1` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `billingAddress2` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `billingCity` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `billingState` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `billingZip` int NOT NULL,
  `billingCountry` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `shippingAddress1` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `shippingAddress2` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `shippingCity` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `shippingState` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `shippingZip` int NOT NULL,
  `shippingCountry` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `company` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`customerID`),
  CONSTRAINT `validPhoneNumber` CHECK ((not((`phone` like _utf8mb4'%[^0-9]%'))))
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


CREATE TABLE `quotes` (
  `quoteID` int NOT NULL AUTO_INCREMENT,
  `item` varchar(255) DEFAULT NULL,
  `customerID` int NOT NULL,
  `prefer` varchar(255) DEFAULT NULL,
  `productID` int NOT NULL,
  `quotePrice` float NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`quoteID`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `quote_items` (
  `id` int NOT NULL,
  `itemID` int NOT NULL,
  PRIMARY KEY (`id`,`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `items` (
  `itemID` int NOT NULL AUTO_INCREMENT,
  `itemName` varchar(45) NOT NULL,
  `price` float NOT NULL,
  `itemDesc` varchar(255) DEFAULT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`itemID`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `inventory` (
    `inventoryID` int NOT NULL AUTO_INCREMENT,
    `inventoryItem` varchar(255) COLLATE utf8_bin NOT NULL,
    `providedByCustomer` varchar(255) COLLATE utf8_bin NOT NULL,
    `customerID` int NOT NULL AUTO_INCREMENT,
    `descriptionOfItem` varchar(1000) COLLATE utf8_bin NOT NULL,
    `inventoryDateObtained` DATE NOT NULL,
    `inventoryDateReleased` DATE NOT NULL,
    `materialOfItem` varchar(255) COLLATE utf8_bin NOT NULL,
    `quantity` int NOT NULL AUTO_INCREMENT,
    `carrier` varchar(20) COLLATE utf8_bin NOT NULL,
    `manufacturerPN` int NOT NULL AUTO_INCREMENT,
    `signedBy` varchar(255) COLLATE utf8_bin NOT NULL,
    FOREIGN KEY `customerID` REFERENCES customers(`customerID`),
    PRIMARY KEY (`inventoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;

CREATE TABLE `ShippingAccounts` (
	`shippingAccountNumber` int NOT NULL AUTO_INCREMENT,
    `nameOfShippingAccount` varchar(255) COLLATE utf8_bin NOT NULL,
	`customerID` int NOT NULL AUTO_INCREMENT,
	`companyID` int NOT NULL AUTO_INCREMENT,
    `carrier` varchar(20) COLLATE utf8_bin NOT NULL,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `address` varchar(255) COLLATE utf8_bin NOT NULL,
    `address2` varchar(255) COLLATE utf8_bin NOT NULL,
    `companyName` varchar(255) COLLATE utf8_bin NOT NULL,
	`phoneNumber` int NOT NULL AUTO_INCREMENT,
    FOREIGN KEY `customerID` REFERENCES customers(`customerID`),
    FOREIGN KEY `companyID` REFERENCES companies(`companyID`),
	PRIMARY KEY (`shippingAccountNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;

CREATE TABLE `orders` (
  `salesperson` varchar(50) DEFAULT NULL,
  `requestor` varchar(45) DEFAULT NULL,
  `customer contact` varchar(15) DEFAULT NULL,
  `reorder` tinyint DEFAULT NULL,
  `factoryOrderQuantity` int NOT NULL,
  `cpInvoice` tinyint DEFAULT NULL,
  `cpPackingSlip` varchar(45) DEFAULT NULL,
  `cpQuantity` int NOT NULL,
  `cpUnitPrice` int DEFAULT NULL,
  `cpTotalPrice` int DEFAULT NULL,
  `niName` varchar(45) DEFAULT NULL,
  `niInvoice` varchar(45) DEFAULT NULL,
  `niPackingSlip` varchar(45) DEFAULT NULL,
  `niQuantity` int DEFAULT NULL,
  `niUnitPrice` int DEFAULT NULL,
  `niTotalPrice` int DEFAULT NULL,
  `iInvoice` varchar(45) DEFAULT NULL,
  `iPackingSlip` varchar(45) DEFAULT NULL,
  `iQuantity` int DEFAULT NULL,
  `iUnitPrice` int DEFAULT NULL,
  `iTotalPrice` int DEFAULT NULL,
  `assemblyCharges` int DEFAULT NULL,
  `acUnitPrice` int DEFAULT NULL,
  `acTotalPrice` int DEFAULT NULL,
  `dcPrintCharge` int DEFAULT NULL,
  `dcSetCharge` int DEFAULT NULL,
  `numOfScreen` int DEFAULT NULL,
  `nosQuantity` int DEFAULT NULL,
  `nosTotalPrice` int DEFAULT NULL,
  `subTotal` int DEFAULT NULL,
  `taxable` tinyint DEFAULT NULL,
  `taxRate` int DEFAULT NULL,
  `taxMoney` int DEFAULT NULL,
  `freightCharges` varchar(45) DEFAULT NULL,
  `ordPriceTotal` int DEFAULT NULL,
  `iiInvoiceDate` varchar(45) DEFAULT NULL,
  `iiDatePaid` int DEFAULT NULL,
  `iiNotes` varchar(45) DEFAULT NULL,
  `salesOrdDate` varchar(45) DEFAULT NULL,
  `custOrdDate` varchar(45) DEFAULT NULL,
  `custPODate` varchar(45) DEFAULT NULL,
  `custPONum` varchar(45) DEFAULT NULL,
  `creditChecked` tinyint DEFAULT NULL,
  `daysTurn` int DEFAULT NULL,
  `dateCodePrint` int DEFAULT NULL,
  `assemBy` varchar(45) DEFAULT NULL,
  `discManBy` varchar(45) DEFAULT NULL,
  `cd-rDVD` varchar(45) DEFAULT NULL,
  `custProvMat` varchar(45) DEFAULT NULL,
  `custMatETA` varchar(45) DEFAULT NULL,
  `custNotes` varchar(255) DEFAULT NULL,
  `vendorNotes` varchar(255) DEFAULT NULL,
  `orderNotes` varchar(255) DEFAULT NULL,
  `orderStatusSub` tinyint DEFAULT NULL,
  `customerID` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
AUTO_INCREMENT=1 ;