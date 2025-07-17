import requests
import json

# Scrape.do API token and target URL
TOKEN = "<your-token>"
TARGET_URL = "https://www.doordash.com/graphql/addConsumerAddressV2?operation=addConsumerAddressV2"

# Build the Scrape.do API URL (no payload/body encoding, just the target URL)
api_url = (
    "http://api.scrape.do/?"
    f"token={TOKEN}"
    f"&super=true"
    f"&url={requests.utils.quote(TARGET_URL)}"
)

# GraphQL mutation payload (as a Python dict for clarity)
payload = {
    "query": """
    mutation addConsumerAddressV2(
      $lat: Float!, $lng: Float!, $city: String!, $state: String!, $zipCode: String!,
      $printableAddress: String!, $shortname: String!, $googlePlaceId: String!,
      $subpremise: String, $driverInstructions: String, $dropoffOptionId: String,
      $manualLat: Float, $manualLng: Float, $addressLinkType: AddressLinkType,
      $buildingName: String, $entryCode: String, $personalAddressLabel: PersonalAddressLabelInput,
      $addressId: String
    ) {
      addConsumerAddressV2(
        lat: $lat, lng: $lng, city: $city, state: $state, zipCode: $zipCode,
        printableAddress: $printableAddress, shortname: $shortname, googlePlaceId: $googlePlaceId,
        subpremise: $subpremise, driverInstructions: $driverInstructions, dropoffOptionId: $dropoffOptionId,
        manualLat: $manualLat, manualLng: $manualLng, addressLinkType: $addressLinkType,
        buildingName: $buildingName, entryCode: $entryCode, personalAddressLabel: $personalAddressLabel,
        addressId: $addressId
      ) {
        defaultAddress {
          id
          addressId
          street
          city
          subpremise
          state
          zipCode
          country
          countryCode
          lat
          lng
          districtId
          manualLat
          manualLng
          timezone
          shortname
          printableAddress
          driverInstructions
          buildingName
          entryCode
          addressLinkType
          formattedAddressSegmentedList
          formattedAddressSegmentedNonUserEditableFieldsList
          __typename
        }
        availableAddresses {
          id
          addressId
          street
          city
          subpremise
          state
          zipCode
          country
          countryCode
          lat
          lng
          districtId
          manualLat
          manualLng
          timezone
          shortname
          printableAddress
          driverInstructions
          buildingName
          entryCode
          addressLinkType
          formattedAddressSegmentedList
          formattedAddressSegmentedNonUserEditableFieldsList
          __typename
        }
        id
        userId
        timezone
        firstName
        lastName
        email
        marketId
        phoneNumber
        defaultCountry
        isGuest
        scheduledDeliveryTime
        __typename
      }
    }
    """,
    "variables": {
        "googlePlaceId": "D000PIWKXDWA",
        "printableAddress": "99 S Broadway, Saratoga Springs, NY 12866, USA",
        "lat": 43.065749988891184,
        "lng": -73.79078001715243,
        "city": "Saratoga Springs",
        "state": "NY",
        "zipCode": "12866",
        "shortname": "National Museum Of Dance",
        "addressId": "1472738929",
        "subpremise": "",
        "driverInstructions": "",
        "dropoffOptionId": "2",
        "addressLinkType": "ADDRESS_LINK_TYPE_UNSPECIFIED",
        "entryCode": ""
    }
}

# Send the POST request to Scrape.do with the JSON payload in the body
response = requests.post(api_url, data=json.dumps(payload))

# Print the scrape.do-rid header for session ID
scrape_do_rid = response.headers.get("scrape.do-rid")
print(f"scrape.do-rid: {scrape_do_rid}")