from langchain_core.tools import tool
from pydantic import BaseModel
from langchain.messages import SystemMessage

class Body(BaseModel):
    collection_name: str


# @tool
def QuizTool():
    
    sys_message = SystemMessage(
        content=""" 
    flow_name: property_overview
    version: derived_from_code
    steps_dataset_order:
    - requirement
    - fuelType
    - boilerType
    - convertToCombi
    - boilerCondition
    - mountedOnWall
    - boilerAge
    - stayDuration
    - waterFlowRate
    - currentBoilerLocation
    - differentPlace
    - airingCupboardLocation
    - newBoilerLocation
    - homeType
    - bungalowFloors
    - flatOnSecondFloor
    - accessEquipmentCharges
    - bedrooms
    - bathtubs
    - bathtubShowerOver
    - showers
    - electricShower
    - powerShower
    - pumpSeparatedFromShower
    - radiators
    - trv
    - waterMeter
    - flueGroundDistance
    - fluePropertyDistance
    - flueUnderStructure
    - flueDoorWindowDistance
    final_step_after_questions: postcode_form

    questions_and_options:
    requirement:
        question: "Are you a homeowner or landlord?"
        options: ["Homeowner", "Landlord"]

    fuelType:
        question: "What kind of fuel does your boiler use?"
        options: ["Gas", "LPG", "Oil"]
        special:
        - if "Oil" => redirect "/boilers/callout/oil"

    boilerType:
        question: "Currently, what type of boiler do you have?"
        options: ["Combi", "Standard", "System", "Back Boiler"]
        special:
        - if "Combi" => jump boilerCondition (skip convertToCombi)
        - else => normal next (convertToCombi)

    convertToCombi:
        question: "Do you want to convert to a Combi boiler?"
        options: ["Yes", "No"]
        special:
        - if answer "No" AND boilerType=="Back Boiler" => redirect "/boilers/callout"
        - otherwise => jump boilerCondition

    boilerCondition:
        question: "How would you describe your current boiler?"
        options: ["Not working", "Old & inefficient", "Doesn't fit with our plans", "Other"]
        next: mountedOnWall

    mountedOnWall:
        question: "Is your boiler mounted on the wall?"
        options: ["Yes it is wall mounted", "No it is floor standing"]
        next: boilerAge

    boilerAge:
        question: "Roughly how old is your boiler?"
        options: ["Up to 10 years", "10-20 years", "20-25 years", "25+ years", "I don't know"]

    stayDuration:
        question: "How long do you see yourself in your current home?"
        options: ["Up to 1 years", "1-5 years", "6-10 years", "10+ years", "I don't know"]

    waterFlowRate:
        question: "How quickly does your water come out of your cold tap?"
        options: ["Fast", "Average", "Slow"]
        special:
        - if "Slow" => redirect "/boilers/callout"

    currentBoilerLocation:
        question: "Where's your current boiler?"
        options: ["Utility room", "Kitchen", "Garage", "Airing cupboard", "Other"]
        special:
        - if "Other" => open free-text prompt (otherRoomName), then continue
        - if pre-existing answers indicate move-somewhere-else with fixed new location => jump homeType
        - otherwise => jump differentPlace

    differentPlace:
        question: "Do you want your new boiler in a different place?"
        options: ["No", "Move to airing cupboard", "Move somewhere else"]
        ui_filter:
        - if currentBoilerLocation=="Airing cupboard", hide option "Move to airing cupboard"
        branching:
        - "Move somewhere else" => jump newBoilerLocation
        - "Move to airing cupboard" => jump airingCupboardLocation
        - "No":
            - if currentBoilerLocation=="Airing cupboard" => jump airingCupboardLocation
            - else => jump homeType

    airingCupboardLocation:
        question: "Where is your airing cupboard?"
        options: ["Middle of the house", "On an outside wall"]
        next: homeType

    newBoilerLocation:
        question: "Where do you want your new boiler?"
        options:
        - "Airing cupboard"
        - "Utility room"
        - "Kitchen"
        - "Garage"
        - "Bathroom"
        - "Bedroom"
        - "Loft or attic"
        - "Somewhere else"
        special:
        - if "Somewhere else" => redirect "/boilers/callout"
        - if "Airing cupboard" => jump airingCupboardLocation
        - else => jump homeType

    homeType:
        question: "Which of these best describes your home?"
        options: ["Detached", "Semi Detached", "Terraced", "Flat", "Bungalow"]
        branching:
        - "Flat" => jump flatOnSecondFloor
        - "Bungalow" => jump bungalowFloors
        - other => jump bedrooms

    bungalowFloors:
        question: "Is your bungalow on one or two floors?"
        options: ["One floor", "Two floors"]
        next: bedrooms

    flatOnSecondFloor:
        question: "Is your flat on or above the second floor?"
        options: ["Yes", "No"]
        branching:
        - "Yes" => jump accessEquipmentCharges
        - "No" => jump bedrooms

    accessEquipmentCharges:
        question: "Do you accept that there may be extra charges for access equipment?"
        options: ["Yes", "No"]
        special:
        - if "No" => redirect "/boilers/callout"
        - if "Yes" => continue to bedrooms

    bedrooms:
        question: "How many bedrooms do you have?"
        options: ["1 bedroom", "2 bedrooms", "3 bedrooms", "4 bedrooms", "5 bedrooms", "6+ bedrooms"]

    bathtubs:
        question: "How many bathtubs do you have, or plan to have in the future?"
        options: ["0 bathtubs", "1 bathtub", "2 bathtubs", "3+ bathtubs"]
        branching:
        - "0 bathtubs" => jump showers
        - else => jump bathtubShowerOver

    bathtubShowerOver:
        question: "Do any of your bathtubs have showers over them?"
        options: ["Yes", "No"]
        next: showers

    showers:
        question: "How many separate showers do you have, or plan to have in the future?"
        options: ["0 showers", "1 shower", "2+ showers"]
        branching:
        - "0 showers" => jump radiators
        - else => jump electricShower

    electricShower:
        question: "Do you have an electric shower?"
        options: ["Yes", "No"]
        branching:
        - "Yes" => jump powerShower
        - "No" => jump radiators

    powerShower:
        question: "Is it a power shower?"
        options: ["Yes", "No"]
        branching:
        - "Yes" => jump pumpSeparatedFromShower
        - "No" => jump radiators

    pumpSeparatedFromShower:
        question: "Is the pump separated from the shower?"
        options: ["Yes", "No", "I don't know"]
        next: radiators

    radiators:
        question: "How many radiators do you have?"
        options: ["0-5 radiators", "6-9 radiators", "10-13 radiators", "14-16 radiators", "17+ radiators"]
        next: trv

    trv:
        question: "Do you have Thermostatic Radiator Valves on all your radiators?"
        options: ["Yes", "No"]
        next: waterMeter

    waterMeter:
        question: "Do you have a water meter?"
        options: ["Yes", "No"]
        next: flueGroundDistance

    flueGroundDistance:
        question: "How close to the ground is your flue?"
        options: ["More than 2 metres", "Less than 2 metres"]
        next: fluePropertyDistance

    fluePropertyDistance:
        question: "How close to another property is your flue?"
        options: ["More than 2 metres", "Less than 2 metres"]
        next: flueUnderStructure

    flueUnderStructure:
        question: "Is the flue under a carport, balcony or other structure?"
        options: ["Yes", "No"]
        next: flueDoorWindowDistance

    flueDoorWindowDistance:
        question: "Is the flue 30cm or more from a door or window?"
        options: ["Yes", "No"]
        next: postcode_form

    postcode_form:
    required_fields:
        - title
        - fastName
        - sureName
        - email
        - mobleNumber
        - postcode
    submit_payload:
        - quizAnswers[]: { question, answer, optional price }

    callout_routes:
    - "/boilers/callout/oil"
    - "/boilers/callout"

    note:
    - There is dead branch code for flueOut/roofType/roofPosition/flueWallDistance/flueShape in container logic, but those steps are commented out in data and are not active.""")

    return sys_message.content