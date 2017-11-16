module.exports.routes = {

  // HTML Views
  // '/': { view: 'homepage' },
  'GET /': 'ContractController.devices',

  'get /login': { view: 'user/login' },
  'get /signup': { view: 'user/signup' },
  '/welcome': { view: 'user/welcome' },

  // '/contracts': {view: 'contracts/contracts'},

  // Endpoints
  'post /login': 'UserController.login',
  'post /signup': 'UserController.signup',
  '/logout': 'UserController.logout',

  'GET /listContracts': 'ContractController.index',
  'POST /addContract': 'ContractController.add',

  'POST /contract/delete/:id': 'ContractController.delete',
  'POST /contract/detail/:id': 'ContractController.detail',
  'GET /contract/detail/:id': 'ContractController.detail',


  'POST /action/add/:id': 'ActionController.add',
  'POST /action/delete/:actionId/:contractId': 'ActionController.delete',

  'GET /setPrice': 'ContractController.setPrice',
  'GET /getPrice': 'ContractController.getPrice',
};
