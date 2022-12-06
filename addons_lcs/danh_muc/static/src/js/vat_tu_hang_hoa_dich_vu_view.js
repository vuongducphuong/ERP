odoo.define('danh_muc.vat_tu_hang_hoa_dich_vu_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var VatTuHangHoaDichVuController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {               
                
                case "btn_cong_thuc_tinh_so_luong":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        //parentID: data.parentID,
                        readonly: this.mode == "readonly",
                        recordID: this.handle,
                        res_model: this.modelName,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Thiết lập công thức tính Số lượng trên chứng từ bán hàng',
                        ref_views: [['danh_muc.view_danh_muc_vat_tu_hang_hoa_thiet_lap_cong_thuc_tinh_so_luong_form', 'form']],
                        size:'medium',
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_after_saved: function (records, changes) {
                            if(changes) {
                                self.changeFieldValue('THIET_LAP_CONG_THUC', records.data.THIET_LAP_CONG_THUC);
                            }
                            
                        },
                    })).open();
                    break;
                case "btn_nhap_don_gia_mua_co_dinh":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        //parentID: data.parentID,
                        readonly: this.mode == "readonly",
                        recordID: this.handle,
                        res_model: this.modelName,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Danh sách đơn giá mua cố định',
                        ref_views: [['danh_muc.view_danh_muc_vat_tu_hang_hoa_don_gia_mua_co_dinh_form', 'form']],
                        size:'medium',
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_after_saved: function (records, changes) {
                            if(changes)
                            {
                                var don_gia_mua_co_dinh ;
                                var don_gia_co_dinh_list = records.data.DANH_MUC_VTHH_DON_GIA_MUA_CO_DINH_IDS.data;
                                var i; 
                                for(i = 0; i < don_gia_co_dinh_list.length; i++){
                                   if(don_gia_co_dinh_list[i].data.currency_id.data.display_name =='VND'){
                                        don_gia_mua_co_dinh = don_gia_co_dinh_list[i].data.DON_GIA;
                                        break;
                                   }
                                } 
                            }
                            self.changeFieldValue('DON_GIA_MUA_CO_DINH',don_gia_mua_co_dinh);
                        },
                    })).open();
                    break;
                
                case "btn_nhap_don_gia_mua_gan_nhat":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        //parentID: data.parentID,
                        readonly: this.mode == "readonly",
                        recordID: this.handle,
                        res_model: this.modelName,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Danh sách đơn giá mua gần nhất',
                        ref_views: [['danh_muc.view_danh_muc_vat_tu_hang_hoa_don_gia_mua_gan_nhat_form', 'form']],
                        size:'medium',
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_after_saved: function (records, changes) {
                            if(changes)
                            {
                                var don_gia_mua_gan_nhat ;
                                var don_gia_mua_gan_nhat_list = records.data.DANH_MUC_VTHH_DON_GIA_MUA_GAN_NHAT_IDS.data;
                                var i; 
                                for(i = 0; i < don_gia_mua_gan_nhat_list.length; i++){
                                   if(don_gia_mua_gan_nhat_list[i].data.currency_id.data.display_name =='VND'){
                                        don_gia_mua_gan_nhat = don_gia_mua_gan_nhat_list[i].data.DON_GIA;
                                        break;
                                   }
                                } 
                            }
                            self.changeFieldValue('DON_GIA_MUA_GAN_NHAT',don_gia_mua_gan_nhat);
                        },
                    })).open();
					break;
                case "btn_nhap_don_gia_ban":
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        //parentID: data.parentID,
                        readonly: this.mode == "readonly",
                        recordID: this.handle,
                        res_model: this.modelName,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        title: 'Nhập đơn giá bán',
                        ref_views: [['danh_muc.view_danh_muc_vat_tu_hang_hoa_nhap_don_gia_ban_form', 'form']],
                        size:'medium',
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_after_saved: function (records, changes) {
                            if(changes)
                            {
                                var don_gia_ban = records.data.GIA_BAN_1;
                                
                            }
                            self.changeFieldValue('DON_GIA_BAN',don_gia_ban);
                        },
                    })).open();
					break;

                case "btn_dsct_phat_sinh_ma_quy_cach":
                    var ma_san_pham = this.getFieldValue('MA');
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        ma_san_pham: ma_san_pham,
                        res_model: 'danh.muc.dsct.phat.sinh.ma.quy.cach.form',
                        title: 'Danh sách chứng từ phát sinh mã quy cách',
                        ref_views: [['danh_muc.view_danh_muc_dsct_phat_sinh_ma_quy_cach_form_tham_so_form', 'form']],
                        size:'large',
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_after_saved: function (records, changes) {
                            
                        },
                    })).open();
                    break;
                default: 
                    this._super.apply(this, arguments);
            }
            
        },
        
    });

    var VatTuHangHoaDichVuRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var VatTuHangHoaDichVuModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var VatTuHangHoaDichVuView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: VatTuHangHoaDichVuModel,
            Renderer: VatTuHangHoaDichVuRenderer,
            Controller: VatTuHangHoaDichVuController,
        }),
    });
    
    view_registry.add('vat_tu_hang_hoa_dich_vu_view', VatTuHangHoaDichVuView);
    
    return VatTuHangHoaDichVuView;
});
