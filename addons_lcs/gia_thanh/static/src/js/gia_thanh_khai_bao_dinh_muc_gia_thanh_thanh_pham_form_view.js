odoo.define('gia_thanh.khai_bao_dinh_muc_gia_thanh_thanh_pham_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var KhaiBaoDinhMucGiaThanhThanhPhamFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			
            this.rpc_action({
                model: 'gia.thanh.khai.bao.dinh.muc.gttp.form',
                method: 'lay_du_lieu_gia_thanh_khai_bao_dinh_muc',
                args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
									
                }
            });
			def.resolve();
        },
    });
    
    var KhaiBaoDinhMucGiaThanhThanhPhamFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: KhaiBaoDinhMucGiaThanhThanhPhamFormController,
        }),
    });
    
    view_registry.add('khai_bao_dinh_muc_gia_thanh_thanh_pham_form_view', KhaiBaoDinhMucGiaThanhThanhPhamFormView);
    
    return KhaiBaoDinhMucGiaThanhThanhPhamFormView;
});
