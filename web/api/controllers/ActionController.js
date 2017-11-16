/**
 * ActionController
 *
 * @description :: Server-side logic for managing actions
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {
	add: function(req, res) {
		// add action to contract
		var contractId = req.param('id')

		if (req.session.isOwner && contractId) {
			// Create an action on a contract
			Action.create({
				contractId: contractId,
				name: req.param('name'),
				description: req.param('description'),
				type: req.param('type'),
				price: req.param('price'),
				scriptHash: req.param('scriptHash')
			}).exec(function (err, record) {
				if (err) {
					console.log(err);
					return res.serverError(err);
				}

				sails.log(req.session.email + ' created record with id:' + record.id);
				// return res.ok();
				return res.redirect('/contract/detail/'+contractId);
			});
		} else {
			return res.ok('permission denied');
		}
	},
	delete: function(req, res) {
		// delete action from contract
		var contractId = req.param('contractId')
		var actionId = req.param('actionId')

		if (req.session.isOwner && actionId) {

			Action.destroy({ id: actionId }).exec(function (err){
			// Action.destroy({}).exec(function (err){
				if (err) {
					return res.negotiate(err);
				}
				sails.log(req.session.email + ' deleted action from actions with id: '+actionId);

				return res.redirect('/contract/detail/'+contractId);
			});
		} else {
			return res.ok('permission denied');
		}
	},
};
