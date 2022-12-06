odoo.define('bao_cao.bao_cao_chi_tiet_cong_no_phai_tra_ncc_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoChiTietCongNoPhaiTraController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
              
                case 'NHOM_NCC_ID':
                    val = this.getFieldValue('MA_PC_NHOM_NCC');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_KH_NCC','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('NHA_CUNG_CAP_MANY_IDS').changeDomain(domain);
                    break;
                
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoChiTietCongNoPhaiTraView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoChiTietCongNoPhaiTraController,
        }),
    });
    
    view_registry.add('bao_cao_chi_tiet_cong_no_phai_tra_ncc_view', BaoCaoChiTietCongNoPhaiTraView);
    return BaoCaoChiTietCongNoPhaiTraView;
});
