odoo.define('bao_cao.bao_cao_s35dn_so_chi_tiet_ban_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoS35SoChiTietBanHangController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'NHOM_VTHH_ID':
                    val = this.getFieldValue('MA_PC_NHOM_VTHH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_VTHH','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('SAN_PHAM_MANY_IDS').changeDomain(domain);
                    break;
            
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoS35SoChiTietBanHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoS35SoChiTietBanHangController,
        }),
    });
    
    view_registry.add('bao_cao_s35dn_so_chi_tiet_ban_hang_view', BaoCaoS35SoChiTietBanHangView);
    return BaoCaoS35SoChiTietBanHangView;
});
