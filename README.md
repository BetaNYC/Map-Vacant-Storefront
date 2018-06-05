# Map-Vacant-Storefront
## Project Overview

The vacant storefront map is a tool for Manhattan’s community boards and council members. It enables users to identify commercial addresses where there may currently be no legally operating businesses and to get street-level views of these addresses through Google Street View. Historically, many community boards and council offices have collected storefront data by walking door-to-door throughout their district and counting the number vacant. This tool has the potential to considerably reduce the amount of time these offices spend collecting this data by hand, while providing valuable insights into the economic health of each district. 

## Development Process and Methodology

This map was conceived in collaboration with the Manhattan Borough President’s Office and Manhattan community board staff members. The tool maps commercial buildings based on the Department of City Planning’s PLUTO files and then hides buildings where there is data about legally operating business, revealing where there may be a vacant storefront. Currently vacant storefronts are defined as any commercial unit within a building. Ideally, vacant storefronts will be defined as any ground-floor commercial unit with an entrance that can be seen from the street. 

### Functional Requirements

Users should be able to view a map that highlights each building in Manhattan that contains at least one vacant storefront. When users click on the highlighted building, a pop-up bubble should display the building’s BIN, the number of vacant storefronts in the building, and the addresses of each vacant storefront. Users should also be able to click on a link to scan the Google Street View of the building. 

#### Preferred

Users should be able to drag a bounding box over an area and receive the number of vacant storefronts within that bounding box. Users should also be able to enter a street segment, community district, council district, neighborhood, or borough and receive the number of vacant storefronts within that geographic boundary. 

### Current Dependencies

* QGIS (would like to switch to Carto)
* Department of City Planning (DCP)’s PLUTO file
* Department of Consumer Affairs (DCA’s) Legally Operating Businesses Dataset
* Data scraped from the NYS Licensee database using [this](https://github.com/BetaNYC/Map-Vacant-Storefront/blob/master/Scripts/NYSLicensesSelenium.py) Python script and Geocoded with DCP’s GeoSupport Desktop software
* The Mayor’s Office of Data Analytics (MODA)’s Multi-Agency Permit Dataset (currently under revision; see [this](https://docs.google.com/document/d/1XgQbVEwl0zLXQFyW_IjIYBdYUocXhiK5gqZwEVudlhw/edit) letter to MODA)
* Google Street View API

### Missing Dependencies

* Data about legally operating retail businesses (clothing, shoes, furniture, and books, e.g.)
* Data about legally operating pharmacies

### Current Strategy

We mapped all of the BBLs in the PLUTO dataset that have a [Building Class](http://www1.nyc.gov/assets/finance/jump/hlpbldgcode.html) of K, C7, D6, D7, G3, L1, L8, RC, RK, S, O4, O5, O6 as polygons. We then joined the fields corresponding to businesses with ‘Active’ licenses in the Legally Operating Businesses dataset to the PLUTO dataset according to the corresponding BBLs and hiding the PLUTO polygons (designating a commercial address) when there was a match. The Legally Operating Business dataset includes permits for the following NYC industries:

* Amusement Arcade
* Amusement Device - Permanent
* Amusement Device - Portable
* Amusement Device - Temporary
* Auction House
* Auctioneer
* Bingo Game Operator
* Booting Company
* Car Wash
* Commercial Lessor
* Dealer in Products for the Disabled
* Debt Collection Agency
* Electronic & Home Appliance Service Dealer
* Electronic Cigarette Retail Dealer 
* Electronics Store
* Employment Agency
* Games of Chance
* Gaming Café
* Garage
* Garage and Parking Lot
* General Vendor
* General Vendor Distributor
* Home Improvement Contractor
* Home Improvement Salesperson
* Horse Drawn Cab Driver
* Horse Drawn Cab Owner
* Industrial Laundry
* Industrial Laundry Delivery
* Locksmith
* Locksmith Apprentice
* Newsstand
* Parking Lot
* Pawnbroker
* Pedicab Business
* Pedicab Driver
* Pool or Billiard Room
* Process Server Individual
* Process Serving Agency
* Retail Laundry
* Scale Dealer/Repairer
* Scrap Metal Processor
* Secondhand Dealer Auto
* Secondhand Dealer General
* Sidewalk Café
* Sightseeing Bus
* Sightseeing Guide
* Special Sale (e.g., Going Out of Business, Liquidation, etc.)
* Stoop Line Stand
* Storage Warehouse
* Temporary Street Fair Vendor Permit
* Ticket Seller Business
* Ticket Seller Individual
* Tobacco Retail Dealer
* Tow Truck Company
* Tow Truck Driver
* Tow Truck Exemption

We wrote a script to scrape the Licensing data for Barbershops and Beauty Salons from the NYS Licensee portal, which can be accessed [here](https://github.com/BetaNYC/Map-Vacant-Storefront/blob/master/Scripts/NYSLicensesSelenium.py) This licensee portal is updated daily, but the script takes several hours to run, so we are planning on updating it monthly (see [this](https://docs.google.com/document/d/1iOBE-K8JfdX8VT4Lrc2XCBPJn35XxQDozcZ4z44MWHE/edit) letter to Secretary of State Rosado, asking for data to streamline this).  After we scraped the data from this site, we geocoded it using DCP’s GeoSupport Desktop software (function 1B) to add BBLs and coordinates for each licensed barbershop and beauty shop address. We had to do significant cleaning to the address field to do this - creating separate columns for the house number, street name, and zip code, and dividing the strings in the address field into these columns. This was a lot more complicated when addresses included floor, apartment, suite, or unit numbers; for the most part, these needed to be manually stripped from the address fields. Once we had geocoded these files, we joined barbershops and beauty salons with a license status of ‘Active’ or ‘Expiring soon’ to the PLUTO dataset according to their corresponding BBLs and hiding the PLUTO polygons (designating a commercial address) when there was a match.

The remaining PLUTO polygons should highlight were there may be a vacant storefront. 

We then installed the QGIS go2streetview plug-in (requires a Google Maps API key), which enabled users viewing the map to drag a line on the map towards the street view they’d like to see. Doing so opens a screen that displays the Google Street View at that location. 

## Issues

1. There may be more than one commercial address at a BBL, but the current strategy hides the building from the map if there are any legally operating businesses in that building. This means that buildings that have multiple commercial units and at least one active business will be hidden from the map, even if they have other commercial units in the building that are vacant. 
2. The building class codes that we’ve designated as “commercial” codes include things like Office with Commercial Units - 1 to 6 stories (O5). When a building has this building code class, it does not guarantee that there is actually a commercial unit there. This means that certain buildings may show up on the map as having a vacant storefront even though there are no storefronts, or even commercial units, at that address. 
3. The current strategy does not differentiate between storefronts, second-floor commercial units, basement commercial units, or commercial units inside a building. This means that certain buildings may show up on the map as having a vacant storefront even though the vacancy cannot be seen from the street. 
4. The Multi-Agency Permits database is broken. We're working with MODA to get this fixed. This means that we cannot remove legally operating restaurants from the map. 

## Project Support Team
Lindsay Poirier, BetaNYC. Contact me by emailing me < lindsay@beta.nyc >

## Project Advisors
* Selected District Managers and Board Chairs
* Hector Rivera, Topographical Bureau Associate

## Funders
Alfred P. Sloan Foundation.

## Relevant Links
* https://github.com/BetaNYC/Map-Vacant-Storefront
* https://beta.nyc/2018/05/15/scraping-nys-beauty-salon-and-barbershop-data/ 

## License
CC BY-SA 3.0 US



