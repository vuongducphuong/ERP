odoo.define('tien_luong.tien_luong_bang_cham_cong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongBangChamCongController = FormController.extend({
        onViewLoaded: function (e, defer) {
            if (this.getFieldValue('LOAI_CHAM_CONG') == 'CHAM_CONG_THEO_GIO') {
                var fieldWidget = this.getFieldWidget("TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL_IDS");
                if (fieldWidget.dxHandler) {
                    fieldWidget.dxHandler.columnOption('Ngày công trong kỳ', 'caption', 'Giờ công trong kỳ');
                }
            }
            if (defer) {
                defer.resolve();
            }
        },
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.bang.cham.cong.form',
                readonly: false,
                title: 'Tạo bảng chấm công',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_bang_cham_cong_form_tham_so_form', 'form']
                ],
                size: 'large',
                on_before_saved: function (controller) {
                    self._controller = controller;
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('DON_VI_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn đơn vị.Xin vui lòng chọn lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        var dam_bao_check_du_dieu_kien = true;
                        var hinh_thuc_tao_cham_cong = controller.getFieldValue('HINH_THUC_TAO_CHAM_CONG');
                        var bang_cham_cong = controller.getFieldValue('BANG_CHAM_CONG');
                        if (hinh_thuc_tao_cham_cong == 'LAY_DANH_SACH') {
                            if (!bang_cham_cong) {
                                dam_bao_check_du_dieu_kien = false;
                                error = 'Bảng chấm công dựa trên không được bỏ trống.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            } else {
                                dam_bao_check_du_dieu_kien = true;
                            }
                        }
                        if (dam_bao_check_du_dieu_kien == true) {
                            var thang = controller.getFieldValue('THANG');
                            var nam = controller.getFieldValue('NAM');
                            controller.rpc_action({
                                model: 'tien.luong.bang.cham.cong.form',
                                method: 'kiem_tra_ton_tai_bang_cham_cong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        var string_Thang_Nam = 'Bảng chấm công tháng ' + String(thang) + ' năm ' + String(nam) + ' đã tồn tại. Bạn có muốn xem bảng chấm công đó không?';
                                        Dialog.show_message('', string_Thang_Nam, 'CONFIRM')
                                            .then(function (result_yes_no) {
                                                if (result_yes_no == true) {
                                                    self._controller.closeDialog();
                                                    var options = {
                                                        res_model: 'tien.luong.bang.cham.cong.chi.tiet.master',
                                                        ref_view: 'tien_luong.view_tien_luong_bang_cham_cong_chi_tiet_master_form',
                                                        res_id: result,
                                                        title: 'Bảng chấm công',
                                                    }

                                                    return self.openFormView(options);

                                                }

                                                def.resolve(false);
                                            });

                                    } else {
                                        def.resolve(true);
                                    }
                                }
                            });
                        }

                    }

                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_cham_cong = record.data.TEN_BANG_CHAM_CONG;
                        var ten_loai_cham_cong = record.data.tenLoaiChamCong;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var hinh_thuc_tao_cham_cong = record.data.HINH_THUC_TAO_CHAM_CONG;
                        if (record.data.DON_VI_IDS.data.length > 0) {
                            var arr_list_don_vi = [];
                            for (var i in record.data.DON_VI_IDS.data) {
                                var chi_tiet = record.data.DON_VI_IDS.data[i].data;
                                if (chi_tiet.AUTO_SELECT == true) {
                                    arr_list_don_vi.push(
                                        chi_tiet.DON_VI_ID,

                                    )
                                }

                            }
                        }
                        var bang_cham_cong = record.data.BANG_CHAM_CONG
                        var LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI = record.data.LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI

                        if (bang_cham_cong) {
                            var bang_cham_cong_id = record.data.BANG_CHAM_CONG.data.id;
                        }

                        var context = {
                            'default_ten_bang_cham_cong': ten_bang_cham_cong,
                            'default_loai_cham_cong': ten_loai_cham_cong,
                            'default_LOAI_CHAM_CONG': record.data.LOAI_CHAM_CONG,
                            'default_thang': thang,
                            'default_nam': nam,
                            'default_hinh_thuc_tao_cham_cong': hinh_thuc_tao_cham_cong,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_bang_cham_cong_id': bang_cham_cong_id,
                            'default_LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI': LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongBangChamCongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongBangChamCongController,
        }),
    });

    view_registry.add('tien_luong_bang_cham_cong_form_view', TienLuongBangChamCongView);

    return TienLuongBangChamCongView;
});

odoo.define('tien_luong.tien_luong_bang_cham_cong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongBangChamCongController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.bang.cham.cong.form',
                readonly: false,
                title: 'Tạo bảng chấm công',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_bang_cham_cong_form_tham_so_form', 'form']
                ],
                size: 'large',
                on_before_saved: function (controller) {
                    self._controller = controller;
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('DON_VI_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn đơn vị.Xin vui lòng chọn lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        var dam_bao_check_du_dieu_kien = true;
                        var hinh_thuc_tao_cham_cong = controller.getFieldValue('HINH_THUC_TAO_CHAM_CONG');
                        var bang_cham_cong = controller.getFieldValue('BANG_CHAM_CONG');
                        if (hinh_thuc_tao_cham_cong == 'LAY_DANH_SACH') {
                            if (!bang_cham_cong) {
                                dam_bao_check_du_dieu_kien = false;
                                error = 'Bảng chấm công dựa trên không được bỏ trống.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            } else {
                                dam_bao_check_du_dieu_kien = true;
                            }
                        }
                        if (dam_bao_check_du_dieu_kien == true) {
                            var thang = controller.getFieldValue('THANG');
                            var nam = controller.getFieldValue('NAM');
                            controller.rpc_action({
                                model: 'tien.luong.bang.cham.cong.form',
                                method: 'kiem_tra_ton_tai_bang_cham_cong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        var string_Thang_Nam = 'Bảng chấm công tháng ' + String(thang) + ' năm ' + String(nam) + ' đã tồn tại. Bạn có muốn xem bảng chấm công đó không?';
                                        Dialog.show_message('', string_Thang_Nam, 'CONFIRM')
                                            .then(function (result_yes_no) {
                                                if (result_yes_no == true) {
                                                    self._controller.closeDialog();
                                                    var options = {
                                                        res_model: 'tien.luong.bang.cham.cong.chi.tiet.master',
                                                        ref_view: 'tien_luong.view_tien_luong_bang_cham_cong_chi_tiet_master_form',
                                                        res_id: result,
                                                        title: 'Bảng chấm công',
                                                    }

                                                    return self.openFormView(options);

                                                }

                                                def.resolve(false);
                                            });

                                    } else {
                                        def.resolve(true);
                                    }
                                }
                            });
                        }

                    }

                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_cham_cong = record.data.TEN_BANG_CHAM_CONG;
                        var ten_loai_cham_cong = record.data.tenLoaiChamCong;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var hinh_thuc_tao_cham_cong = record.data.HINH_THUC_TAO_CHAM_CONG;
                        if (record.data.DON_VI_IDS.data.length > 0) {
                            var arr_list_don_vi = [];
                            for (var i in record.data.DON_VI_IDS.data) {
                                var chi_tiet = record.data.DON_VI_IDS.data[i].data;
                                if (chi_tiet.AUTO_SELECT == true) {
                                    arr_list_don_vi.push(
                                        chi_tiet.DON_VI_ID,

                                    )
                                }

                            }
                        }
                        var bang_cham_cong = record.data.BANG_CHAM_CONG
                        var LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI = record.data.LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI

                        if (bang_cham_cong) {
                            var bang_cham_cong_id = record.data.BANG_CHAM_CONG.data.id;
                        }

                        var context = {
                            'default_ten_bang_cham_cong': ten_bang_cham_cong,
                            'default_loai_cham_cong': ten_loai_cham_cong,
                            'default_LOAI_CHAM_CONG': record.data.LOAI_CHAM_CONG,
                            'default_thang': thang,
                            'default_nam': nam,
                            'default_hinh_thuc_tao_cham_cong': hinh_thuc_tao_cham_cong,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_bang_cham_cong_id': bang_cham_cong_id,
                            'default_LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI': LAY_TAT_CA_NHAN_VIEN_DA_NGUNG_THEO_DOI,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongBangChamCongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongBangChamCongController,
        }),
    });

    view_registry.add('tien_luong_bang_cham_cong_list_view', TienLuongBangChamCongView);

    return TienLuongBangChamCongView;
});