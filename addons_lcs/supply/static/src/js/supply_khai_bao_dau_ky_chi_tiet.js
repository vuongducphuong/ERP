odoo.define('supply.supply_khai_bao_dau_ky_chi_tiet_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KhaiBaoDauKyChiTietController = FormController.extend({
        on_before_saved: function() {
            var def = $.Deferred();
            var self = this;
            var list_fields = ['MA_CCDC','TEN_CCDC','NGAY_GHI_TANG'];
            var error = [];
            _.each(list_fields, function(field) {
                var field_val = self.getFieldValue(field);
                if (!field_val || (_.isArray(field_val) && field_val.length == 0)) {
                    error.push({field:field, message:'Không được bỏ trống'});
                }
            })
            if (error.length) {
                this.notifyInvalidFields(error);
                def.resolve(false);
            } else {
                def.resolve(true);
            }
            return def;                      
        },
    });
    
    var KhaiBaoDauKyChiTietView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KhaiBaoDauKyChiTietController,
        }),
    });
    
    view_registry.add('supply_khai_bao_dau_ky_chi_tiet_view', KhaiBaoDauKyChiTietView);
    
    return KhaiBaoDauKyChiTietView;
});
