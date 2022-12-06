odoo.define('stock_ex.stock_ex_lenh_san_xuat_lap_pn_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var Dialog = require('web.Dialog');

    var LenhSanXuatPNController = FormController.extend({

        _onButtonClicked: function (event) {
            var self = this;
            event.stopPropagation();
            switch (event.data.attrs.class) {
                case "btn_phieu_nhap_xuat_kho":
                    var context = {};
                    var default_chi_tiet = [];

                    var current_data = event.data.record.data;
                    var chitiet_ids = current_data.STOCK_EX_LENH_SAN_XUAT_LAP_PN_CHI_TIET_FORM_IDS.data;
                    for (var i = 0; i < chitiet_ids.length; i++) {

                        //chỉ lấy những thằng chọn
                        var chi_tiet = chitiet_ids[i].data;
                        if (chi_tiet.AUTO_SELECT) {
                            //                             default_chi_tiet.push((0,0,{
                            //                                 'MA_HANG_ID' :chi_tiet.MA_THANH_PHAM_ID.res_id,
                            //                                 'TEN_HANG'   :chi_tiet.TEN_THANH_PHAM,
                            //                                 'SO_LUONG'   :chi_tiet.SO_LUONG,
                            //                                 'DVT_ID' :chi_tiet.DVT_ID.res_id,

                            //                             }))
                            default_chi_tiet.push(chi_tiet.LENH_SAN_XUAT_THANH_PHAM_ID);
                        }

                    }

                    if (default_chi_tiet.length == 0) {
                        return new Dialog(this, {
                            size: 'medium',
                            title: 'Thông báo',
                            $content: $('<div>').html('<p>Xin vui lòng chọn ít nhất một dòng </p>'),

                            buttons: [
                                {
                                    text: 'Đồng ý',
                                    close: true,
                                },
                            ],
                        }).open();
                    }


                    context['id_lenh_san_xuat_thanh_pham'] = default_chi_tiet;
                    var tenview = '';
                    var ten_title = '';
                    if (current_data.LENH_SX_PN_PX == 'PHIEU_NHAP') {
                        context['default_type'] = 'NHAP_KHO';
                        context['default_LAP_TU_LENH_SAN_XUAT_PHIEU_XUAT'] = true;
                        context['default_LOAI_NHAP_KHO'] = 'THANH_PHAM';
                        tenview = 'stock_ex.view_nhap_kho_form';
                        ten_title = 'Nhập kho thành phẩm sản xuất';

                    }
                    else {
                        context['default_type'] = 'XUAT_KHO';
                        context['default_LOAI_XUAT_KHO'] = 'SAN_XUAT';
                        context['default_LAP_TU_LENH_SAN_XUAT_PHIEU_XUAT'] = true;
                        tenview = 'stock_ex.view_xuat_kho_form';
                        ten_title = 'Xuất kho thành phẩm sản xuất';
                    }
                    context['default_ID_LSX_LAP_PHIEU_NX'] = current_data.LSX_ID.res_id;
                    return self.openFormView(_.extend({}, this.nodeOptions, {
                        res_model: 'stock.ex.nhap.xuat.kho',
                        // title: 'Nhập kho thành phẩm sản xuất',
                        title: ten_title,
                        ref_view: tenview,
                        context: context,
                    }));

                default:
                    this._super.apply(this, arguments);
            }

        }
    });

    var LenhSanXuatPNView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: LenhSanXuatPNController,
        }),
    });

    view_registry.add('stock_ex_lenh_san_xuat_lap_pn_form_view', LenhSanXuatPNView);

    return LenhSanXuatPNView;
});
