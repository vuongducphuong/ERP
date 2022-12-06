odoo.define('bao_cao.bao_cao_gia_thanh_tong_hop_nxk_theo_doi_tuong_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoNXKTheoDoiTuongController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'THONG_KE_THEO':
                    val = this.getFieldValue('MA_PC_NHOM_VTHH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_VTHH','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('SAN_PHAM_MANY_IDS').changeDomain(domain);
                    break;
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
    
    var BaoCaoNXKTheoDoiTuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoNXKTheoDoiTuongController,
        }),
    });
    
    view_registry.add('bao_cao_gia_thanh_tong_hop_nxk_theo_doi_tuong_view', BaoCaoNXKTheoDoiTuongView);
    return BaoCaoNXKTheoDoiTuongView;
});
