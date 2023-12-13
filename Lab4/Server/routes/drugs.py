from flask import Blueprint
from controllers.drugController import *

blueprint = Blueprint('drugs', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/all', methods=['GET'])(drugs)
blueprint.route('/barcode', methods=['GET'])(readBarcode)
blueprint.route('/add', methods=['POST'])(addDrug)