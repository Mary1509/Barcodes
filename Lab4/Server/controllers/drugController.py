from flask import jsonify, make_response, request, send_file
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from models.drug import Drug
from models.base import Base, db
from models.store import Store
from models.address import Address
from models.type import Type
from models.subst import Substance
from models.mark import Mark
from models.chain import Chain
from models.city import City
from models.user import User
from services.barcode import BarcodeService


def index():
    return 'Drugs index'


def drugs():
    res = []
    try:
        drugs = db.session.query(Drug, Type, Substance, Mark).join(Type).join(Substance).join(Mark).all()
        if not drugs:
            return make_response(jsonify("Error querying drugs"), 404)

        for drug_res in drugs:
            drug_dict = drug_res[0].as_dict()
            type_dict = drug_res[1].as_dict()
            subst_dict = drug_res[2].as_dict()
            mark_dict = drug_res[3].as_dict()

            drug_dict.pop('type_id')
            drug_dict['type'] = type_dict['name']

            drug_dict.pop('main_subs_id')
            drug_dict['subst'] = subst_dict['name']

            drug_dict.pop('trademark_id')
            drug_dict['mark'] = mark_dict['name']

            res.append(drug_dict)
        return make_response(jsonify(res), 200)
    except SQLAlchemyError as e:
        return make_response(jsonify('Error querying drugs'), 500)



    # res = []
    # for shelter_res, address_res in shelters:
    #     dict_shelter = shelter_res.as_dict()
    #     dict_address = address_res.as_dict()
    #     if not dict_address['houseNumber'] is None:
    #         address_str = str(dict_address['street']) + ', ' + str(dict_address['houseNumber'])
    #     else:
    #         address_str = str(dict_address['street'])
    #     dict = {
    #         'id': dict_shelter['id'],
    #         'address': address_str
    #     }
    #     res.append(dict)
    # return make_response(jsonify(res), 200)
    # return "Shelters"


# def drugsWithFilters():
#     types = request.args.getlist('type', None)
#     purposes = request.args.getlist('purpose', None)
#     hasRamp = request.args.get('hasRamp', None)
#
#
#     query = ''
#     if len(types) > 0:
#         types_str = ','.join(types)
#         if len(purposes) > 0:
#             purposes_str = ','.join(purposes)
#             if not hasRamp is None:
#                 shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address)\
#                     .filter(shelter.Shelter.typeId.in_(types[0].split(',')),
#                              shelter.Shelter.purposeId.in_(purposes[0].split(',')),
#                              shelter.Shelter.hasRamp == hasRamp).all()
#             else:
#                 shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                     .filter(shelter.Shelter.typeId.in_(types[0].split(',')),
#                             shelter.Shelter.purposeId.in_(purposes[0].split(','))).all()
#         elif not hasRamp is None:
#             shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                 .filter(shelter.Shelter.typeId.in_(types[0].split(',')), shelter.Shelter.hasRamp == hasRamp).all()
#         else:
#             shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                 .filter(shelter.Shelter.typeId.in_(types[0].split(','))).all()
#     elif len(purposes) > 0:
#         purposes_str = ','.join(purposes)
#         if not hasRamp is None:
#             shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                         .filter(shelter.Shelter.purposeId.in_(purposes[0].split(',')), shelter.Shelter.hasRamp == hasRamp).all()
#         else:
#             shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                         .filter(shelter.Shelter.purposeId.in_(purposes[0].split(','))).all()
#     else:
#         shelters = db.session.query(shelter.Shelter, address.Address).join(address.Address) \
#                     .filter(shelter.Shelter.hasRamp == hasRamp).all()
#
#
#     res = []
#     for shelter_res, address_res in shelters:
#         dict_shelter = shelter_res.as_dict()
#         dict_address = address_res.as_dict()
#         if not dict_address['houseNumber'] is None:
#             address_str = str(dict_address['street']) + ', ' + str(dict_address['houseNumber'])
#         else:
#             address_str = str(dict_address['street'])
#         dict = {
#             'id': dict_shelter['id'],
#             'address': address_str
#         }
#         res.append(dict)
#     return make_response(jsonify(res), 200)


# def getDrugById(id):
#
#     query = text(f"""SELECT  sh.id, latitude, longitude, concat(addresses."street", ', ', addresses."houseNumber") AS address,
#                      shelter_types.type AS type,
#                      shelter_purposes.purpose AS purpose, capacity, sh."hasRamp"
#                      FROM shelters sh
#                      INNER JOIN addresses ON "addressId" = addresses.id
#                      INNER JOIN shelter_types ON "typeId" = shelter_types.id
#                      INNER JOIN shelter_purposes ON "purposeId" = shelter_purposes.id
#                      WHERE sh.id = {id}""")
#     shelter_res = db.session.execute(query).first()
#     res = {}
#     if not shelter_res is None:
#         res = {
#             'id': shelter_res[0],
#             'latitude': shelter_res[1],
#             'longitude': shelter_res[2],
#             'address': shelter_res[3],
#             'type': shelter_res[4],
#             'purpose': shelter_res[5],
#             'capacity': shelter_res[6],
#             'hasRamp': shelter_res[7]
#         }
#     else:
#         return make_response(jsonify(res), 404)
#     return make_response(jsonify(res), 200)


def addDrug():
    drug_raw = request.json
    type = db.session.query(Type).filter(Type.name == drug_raw['type']).first()
    if type is None:
        type = Type(name=drug_raw['type'])
        db.session.add(type)
        db.session.flush()
    mark = db.session.query(Mark).filter(Mark.name == drug_raw['mark']).first()
    if mark is None:
        mark = Mark(name=drug_raw['mark'])
        db.session.add(mark)
        db.session.flush()
    subst = db.session.query(Substance).filter(Substance.name == drug_raw['subst']).first()
    if subst is None:
        subst = Substance(name=drug_raw['subst'])
        db.session.add(subst)
        db.session.flush()

    code_list = [mark.uid, subst.uid, type.uid]
    code = '-'.join(map(str, code_list))

    drug = Drug(name=drug_raw['name'],
                barcode=code,
                exp_date=drug_raw['exp_date'],
                serial_no=drug_raw['serial_no'],
                prescription=drug_raw['prescription'],
                type_id=type.uid,
                main_subs_id=subst.uid,
                trademark_id=mark.uid)
    drug.mark = mark
    drug.subs = subst
    drug.type = type

    # generate barcode

    try:
        db.session.add(drug)
        db.session.commit()
        BarcodeService.generate(code)
        return send_file('result.png', mimetype='image/png')
    except Exception as err:
        print(err)
        return make_response(jsonify({'message': 'Error generating', 'error': f'{err}'}), 503)


# def delDrug(id):
#     try:
#         shelter_res = db.session.query(shelter.Shelter).filter_by(id=int(id)).delete()
#         db.session.commit()
#         if shelter_res == 0:
#             return make_response(jsonify(shelter_res), 404)
#         return make_response(jsonify(shelter_res), 201)
#     except SQLAlchemyError as e:
#         error = str(e.__dict__['orig'])
#         return make_response(jsonify(error), e.code)


def readBarcode():
    # call service with barcode reader
    barcode_file = request.files['barcode_file']
    barcode_file.save('barcode_file.png')
    barcode = BarcodeService.scan('barcode_file.png')
    if barcode is None:
        print("No barcode")
        return make_response(jsonify({'message': 'No barcode found in image'}), 400)
    else:
        try:
            drug = (db.session.query(Drug, Type, Substance, Mark).
                    join(Type).join(Substance).join(Mark).filter(Drug.barcode == barcode)).first()
            if drug is None:
                return make_response(jsonify({'message': 'No barcode found in database'}), 404)
            else:
                drug_dict = drug[0].as_dict()
                type_dict = drug[1].as_dict()
                subst_dict = drug[2].as_dict()
                mark_dict = drug[3].as_dict()

                drug_dict.pop('type_id')
                drug_dict['type'] = type_dict['name']

                drug_dict.pop('main_subs_id')
                drug_dict['subst'] = subst_dict['name']

                drug_dict.pop('trademark_id')
                drug_dict['mark'] = mark_dict['name']
                print(drug_dict)
                return make_response(jsonify(drug_dict), 200)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return make_response(jsonify(error), e.code)

