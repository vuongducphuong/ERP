odoo.define('sale_ex.chung_tu_ban_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChungTuBanHangController = FormController.extend({

        _onOpenLink: function(event) {
            var record = this.model.get(event.data.recordId);
            var lap_rap = record.data.LAP_RAP_ID;
            return this.openFormView({
                res_model: lap_rap.model,
                res_id: lap_rap.data.id,
                context: {open_copy: true},
            });
        },

        _onButtonClicked: function (event) {
            var self = this;
            event.stopPropagation();
            switch (event.data.attrs.id) {

                case "btn_phan_bo_chiet_khau_ban_hang":
                    var context = {};
                    var default_chi_tiet = [];
                    // Lấy data hiện tại của form
                    var current_data = event.data.record.data;
                    // Lấy data của chứng từ chi tiết
                    var currency_id_master = this.getFieldValue('currency_id');
                    var chi_tiet_ids = this.getFieldValue('SALE_DOCUMENT_LINE_IDS');
                    for (var i = 0; i < chi_tiet_ids.length; i++) {
                        var chi_tiet = chi_tiet_ids[i];
                        self.updateUI({ 'SALE_DOCUMENT_LINE_IDS': [[1, chi_tiet.res_id, { 'INDEX': i }]] });
                        default_chi_tiet.push([0, 0, {
                            'MA_HANG_ID': chi_tiet.MA_HANG_ID.id,
                            'TEN_HANG': chi_tiet.TEN_HANG,
                            'SO_LUONG': chi_tiet.SO_LUONG,
                            'THANH_TIEN': chi_tiet.THANH_TIEN,
                            'INDEX': i,
                            'currency_id' : chi_tiet.currency_id.id,
                        }])
                    }
                    context['default_SALE_EX_PHAN_BO_CHIET_KHAU_THEO_TONG_GIA_TRI_HOA_DON_CHI_TIET_IDS'] = default_chi_tiet;
                    context['default_currency_id'] = currency_id_master.id;
                    return new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'sale.ex.phan.bo.chiet.khau.theo.tong.gia.tri.hd.form',
                        title: 'Phân bổ chiết khấu theo tổng giá trị hóa đơn',
                        ref_views: [['sale_ex.view_sale_ex_ban_hang_phan_bo_chiet_khau_theo_tong_gia_tri_hoa_don_form_form', 'form']],
                        context: context,
                        on_selected: function (records, handle) {
                            self.changeFieldValue('PHAN_BO_CHIET_KHAU_JSON', records);
                            self.closeDialog(handle);
                        },
                    })).open();

                default:
                    this._super.apply(this, arguments);
            }

        },
        onViewLoaded: function (e, defer) {
            this._changeChiTietSelection();
            if (defer) {
                defer.resolve();
            }
        },

        _changeChiTietSelection: function() {
            if (this.getFieldValue('KIEM_PHIEU_NHAP_XUAT_KHO')) {
                this.changeSelectionSource('chi_tiet', ['hang_tien', 'thue', 'gia_von', 'thong_ke']);
            } else {
                this.changeSelectionSource('chi_tiet', ['hang_tien', 'thue', 'thong_ke']);
            }
        },

        onFieldChanged: function (field) {
            switch (field) {
                case 'CHON_LAP_TU_ID':
                    var fieldWidget = this.getFieldWidget(field);
                    var fieldValue = this.getFieldValue(field);
                    if (fieldValue.model == "stock.ex.nhap.xuat.kho,Lập từ Phiếu xuất") {
                        fieldWidget.changeDomain([['type', '=', 'XUAT_KHO']], true);
                    }
                    else if (fieldValue.model == "stock.ex.nhap.xuat.kho,Lập từ Chuyển kho") {
                        fieldWidget.changeDomain([['type', '=', 'CHUYEN_KHO']], true);
                    }
                    else if (fieldValue.model == "account.ex.don.dat.hang,Lập từ Đơn đặt hàng") {
                        fieldWidget.changeDomain(['|',['TINH_TRANG', '=', '0'],['TINH_TRANG', '=', '1']], true);
                    }
                    else if (fieldValue.model == "sale.ex.hoa.don.ban.hang,Lập từ Hóa đơn") {
                        var loai_nghiep_vu_ban_hang = this.getFieldValue('LOAI_NGHIEP_VU')
                        var loai_chung_tu = this._get_loai_chung_tu(loai_nghiep_vu_ban_hang);
                        fieldWidget.changeDomain([['DA_HACH_TOAN', '=', false],['LOAI_CHUNG_TU', '=', loai_chung_tu]], true);
                    }
                    else {
                        fieldWidget.changeDomain([]);
                    }
                    break;
                case 'KIEM_PHIEU_NHAP_XUAT_KHO':
                    this._changeChiTietSelection();
                    break;
                case 'LOAI_NGHIEP_VU':
                    var fieldWidget = this.getFieldWidget('CHON_LAP_TU_ID');
                    var fieldValue = this.getFieldValue('CHON_LAP_TU_ID');
                    var loai_nghiep_vu_ban_hang = this.getFieldValue('LOAI_NGHIEP_VU');
                    var loai_chung_tu = this._get_loai_chung_tu(loai_nghiep_vu_ban_hang);
                    if (fieldValue && fieldValue.model == "sale.ex.hoa.don.ban.hang,Lập từ Hóa đơn"){
                        fieldWidget.changeDomain([['DA_HACH_TOAN', '=', false],['LOAI_CHUNG_TU', '=', loai_chung_tu]], true);
                    }
                    break;
                case 'DOI_TUONG_ID':
                    var fieldValue = this.getFieldValue(field);
                    this.getFieldWidget('TK_NGAN_HANG').changeDomain([['DOI_TUONG_ID', '=', fieldValue.id]]);
                    break;
                default:
                    break;
            }
        },

        // Hàm lấy loại chứng từ của hóa đơn khi nghiệp vụ bán hàng thay đổi 
        _get_loai_chung_tu: function(loai_nghiep_vu_ban_hang) {
            var self = this;
            var loai_chung_tu;
            if (loai_nghiep_vu_ban_hang == 'TRONG_NUOC'){
                loai_chung_tu = 3560;
            }
            else if (loai_nghiep_vu_ban_hang == 'XUAT_KHAU'){
                loai_chung_tu = 3561;
            }
            else if (loai_nghiep_vu_ban_hang == 'DAI_LY'){
                loai_chung_tu = 3562;
            }
            else if (loai_nghiep_vu_ban_hang == 'UY_THAC'){
                loai_chung_tu = 3563;
            }
            return loai_chung_tu;
        }
    });

    var ChungTuBanHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChungTuBanHangController,
        }),
    });

    view_registry.add('chung_tu_ban_hang_view', ChungTuBanHangView);

    return ChungTuBanHangView;
});
