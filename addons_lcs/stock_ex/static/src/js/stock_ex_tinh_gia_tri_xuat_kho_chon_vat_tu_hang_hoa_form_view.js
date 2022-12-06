odoo.define('stock_ex.tinh_gia_tri_xuat_kho_chon_vat_tu_hang_hoa_form', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var TinhGiaXuatKhoChonVatTuHangHoaController = FormController.extend({
        onViewLoaded: function(e, defer) {
            var self = this;
            var def = defer;
            this.rpc_action({
                model: 'stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.form',
                method: 'load_du_lieu',
                callback: function(result) {
                    if (result) {
                        self.updateUI({'STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM_IDS': result});
                    }
					if (def) {
                        def.resolve();
                    }					
                }
            });
        }
    });
    
    var TinhGiaXuatKhoChonVatTuHangHoaView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TinhGiaXuatKhoChonVatTuHangHoaController,
        }),
    });
    
    view_registry.add('tinh_gia_tri_xuat_kho_chon_vat_tu_hang_hoa_form', TinhGiaXuatKhoChonVatTuHangHoaView);
    
    return TinhGiaXuatKhoChonVatTuHangHoaView;
});