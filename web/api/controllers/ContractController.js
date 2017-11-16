/**
 * ContractController
 *
 * @description :: Server-side logic for managing contracts
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {
		index: function(req, res) {
			Contract.find({}).exec(function(err, contracts) {
				res.view('contracts/contracts', {
				  // mock it
					// contracts: [{id: 1, name: 'test', description: 'test', address: 'aldkjlzkcjvif', walletAddress: 'aldkjfirufj'}]
					contracts: contracts
			});
		});
	},

	detail: function(req, res) {
		// show details of contract
		var id = req.param('id')

		if (req.session.isOwner && id) {
			Contract.findOne({id: id}).exec(function(err, contract) {
				Action.find({contractId: id}).exec(function(err, actions) {

					if (actions) {
						res.view('contracts/detail', {
							// mock it
							// contracts: [{id: 1, name: 'test', description: 'test', address: 'aldkjlzkcjvif', walletAddress: 'aldkjfirufj'}]
							contract: contract,
							actions: actions
						});
					} else {
						res.view('contracts/detail', {
							// mock it
							// contracts: [{id: 1, name: 'test', description: 'test', address: 'aldkjlzkcjvif', walletAddress: 'aldkjfirufj'}]
							contract: contract,
							actions: null
						});
					}
				});
			});
		}
	},
	devices: function(req, res) {
		// show details of contract
		// var id = req.param('id')

		if (req.session.isOwner) {
			Action.find({}).exec(function(err, actions) {

				if (actions) {
					res.view('devices', {
						actions: actions
					});
				} else {
					res.view('devices', {
						actions: null
					});
				}
			});
		}
	},
	add: function(req, res) {
		// dispatch contract invocation to add storage value to contract
		// OWNER ONLY - must be logged into extension
		if (req.session.isOwner) {
			// Create a user
			Contract.create({
				name: req.param('name'),
				description: req.param('description'),
				scriptHash: req.param('scriptHash'),
				ownerEmail: req.session.email
			}).exec(function (err, record) {
  			if (err) { return res.serverError(err); }

  			sails.log(req.session.email + ' created record with id:' + record.id);
  			// return res.ok();
				return res.redirect('/listContracts');
			});
		} else {
			return res.ok('permission denied');

		}
	},
	delete: function(req, res) {
		// dispatch contract invocation to delete storage value from contract
		// OWNER ONLY - must be logged into extension
		var id = req.param('id')
		if (req.session.isOwner && id) {

			Contract.destroy({ id: id }).exec(function (err){
	  		if (err) {
	    		return res.negotiate(err);
	  		}
	  		sails.log(req.session.email + ' deleted contract with id: '+id);
	  		// return res.ok();
				return res.redirect('/listContracts');

			});
		} else {
			return res.ok('permission denied');
		}
	},
	setPrice: function(req, res) {
		// dispatch contract invocation to set price
		// OWNER ONLY - must be logged into extension
	},
	getPrice: function(req, res) {
		// dispatch contract invocation to get price
		// anyone and doesnt require that user is logged into extension

	},

};
