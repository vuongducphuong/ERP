odoo.define('stock_ex.stock_ex_tinh_gia_xuat_kho_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TinhGiaXuatKhoController = FormController.extend({

        _onButtonClicked: function(event) {
            var self = this;
            var record = event.data.record;
            event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_chon":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        readonly: this.mode == "readonly",
                        recordID: record.id,
                        res_model: 'stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.form',
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Chọn vật tư, hàng hóa tính giá xuất',
                        ref_views: [['stock_ex.view_stock_ex_tinh_gia_xuat_kho_chon_vat_tu_hang_hoa_form_tham_so_form', 'form']],
                        size:'huge',
                        on_after_saved: function (records, changes) {
                            if(changes)
                            {
                                var list_vthh = ';';
                                var chon_vthh_ids = records.data.STOCK_EX_TINH_GIA_XUAT_KHO_CHON_VAT_TU_HANG_HOA_CHI_TIET_FORM_IDS.data;
                                for(var i = 0; i< chon_vthh_ids.length;i++){
                                    var chon_vthh = chon_vthh_ids[i].data;
                                    if(chon_vthh.AUTO_SELECT == true){
                                        list_vthh += chon_vthh.MA_VAT_TU_HANG_HOA_ID.data.id;
                                        list_vthh += ';';
                                    }
                                };
                                self.changeFieldValue('LIST_VTHH', list_vthh);
                            }
                        },
                    })).open();
                    break;
                //    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                //         res_model: 'stock.ex.tinh.gia.xuat.kho.chon.vat.tu.hang.hoa.form',
                //         title: 'Chọn vật tư. hàng hóa tính giá xuất',
                //         ref_views: [['stock_ex.view_stock_ex_tinh_gia_xuat_kho_chon_vat_tu_hang_hoa_form_tham_so_form', 'form']],
                //         // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                //         on_selected: function (records) {
                //             self.changeFieldValue('CHON_CHI_PHI_JSON', records)
                //         }, 
                //     })).open();
                case "btn_thuc_hien":
                    var tu_ngay = false;
                    var den_ngay = false;
                    if(this.getFieldValue('TU_NGAY')){
                        tu_ngay = this.getFieldValue('TU_NGAY')
                    };
                    if(this.getFieldValue('TU_NGAY')){
                        den_ngay = this.getFieldValue('TU_NGAY')
                    };
                    this.rpc_action({
                        model: 'stock.ex.tinh.gia.xuat.kho',
                        method: 'btn_tinh_gia_xuat_kho',
                        args: {
                            'tu_ngay' : tu_ngay,
                            'den_ngay' : den_ngay,
                        },
                        callback: function(result) {
                            if (result) {
                                Dialog.show_message('tieu_de', 'Tính giá xuất kho hoàn thành', 'ALERT')
                                .then(function(result) {
                                    // Xử lý sau khi đóng popup
                                });
                            }
                        }
                    });
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var TinhGiaXuatKhoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TinhGiaXuatKhoController,
        }),
    });
    
    view_registry.add('stock_ex_tinh_gia_xuat_kho_view', TinhGiaXuatKhoView);
    
    return TinhGiaXuatKhoView;
});
