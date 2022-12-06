odoo.define('tien_ich.ghi_so_bo_ghi_so_theo_lo_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var GhiSoBoGhiSoTheoLoController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
       
        onViewLoaded: function(e, defer) {
			var def = defer;
            var self = this;
            this.rpc_action({
                model: 'tien.ich.ghi.so.hoac.bo.ghi.so.theo.lo',
                method: 'load_phan_he',
                // args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
					if (def) {
                        def.resolve();
                    }		
                }
            });
        },
       
    });



    
    var GhiSoBoGhiSoTheoLoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: GhiSoBoGhiSoTheoLoController,
        }),
    });
    
    view_registry.add('ghi_so_bo_ghi_so_theo_lo_view', GhiSoBoGhiSoTheoLoView);
    
    return GhiSoBoGhiSoTheoLoView;
});
