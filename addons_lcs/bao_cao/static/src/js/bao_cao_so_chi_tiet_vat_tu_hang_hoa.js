odoo.define('bao_cao.bao_cao_so_chi_tiet_vat_tu_hang_hoa_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoSoChiTietVatTuHangHoaController = FormController.extend({
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
    
    var BaoCaoSoChiTietVatTuHangHoaView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoSoChiTietVatTuHangHoaController,
        }),
    });
    
    view_registry.add('bao_cao_so_chi_tiet_vat_tu_hang_hoa_view', BaoCaoSoChiTietVatTuHangHoaView);
    return BaoCaoSoChiTietVatTuHangHoaView;
});
