odoo.define('bao_cao.bao_cao_so_chi_tiet_tai_khoan_theo_doi_tuong_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoSoChiTietTKTheoDoiTuongController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'NHOM_KH_NCC_ID':
                    val = this.getFieldValue('MA_PC_NHOM_KH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_KH_NCC','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('DOI_TUONG_MANY_IDS').changeDomain(domain);
                    this.getFieldWidget('NHA_CUNG_CAP_MANY_IDS').changeDomain(domain);
                    this.getFieldWidget('KHACH_HANG_MANY_IDS').changeDomain(domain);
                    break;
                
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoSoChiTietTKTheoDoiTuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoSoChiTietTKTheoDoiTuongController,
        }),
    });
    
    view_registry.add('bao_cao_so_chi_tiet_tai_khoan_theo_doi_tuong_view', BaoCaoSoChiTietTKTheoDoiTuongView);
    return BaoCaoSoChiTietTKTheoDoiTuongView;
});
