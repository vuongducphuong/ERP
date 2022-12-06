odoo.define('bao_cao.bao_cao_gia_thanh_bang_ke_phieu_nhap_xuat_theo_doi_tuong_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoPNXTheoDoiTuongController = FormController.extend({
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
    
    var BaoCaoPNXTheoDoiTuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoPNXTheoDoiTuongController,
        }),
    });
    
    view_registry.add('bao_cao_gia_thanh_bang_ke_phieu_nhap_xuat_theo_doi_tuong_view', BaoCaoPNXTheoDoiTuongView);
    return BaoCaoPNXTheoDoiTuongView;
});
