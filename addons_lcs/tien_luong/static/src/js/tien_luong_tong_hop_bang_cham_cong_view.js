odoo.define('tien_luong.tien_luong_tong_hop_bang_cham_cong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var TienLuongTongHopBangChamCongController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.tong.hop.cham.cong.tham.so',
                readonly: false,
                title: 'Tổng hợp chấm công',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_tong_hop_cham_cong_tham_so_tham_so_form', 'form']
                ],
                size: 'large',
                on_before_saved: function (controller) {
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
                        var thang = controller.getFieldValue('THANG');
                        var nam = controller.getFieldValue('NAM');
                        var dam_bao_check_du_dieu_kien = true;
                        var tong_hop_tu_cac_bang_cham_cong_chi_tiet = controller.getFieldValue('TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET');
                        if (tong_hop_tu_cac_bang_cham_cong_chi_tiet == true) {
                            controller.rpc_action({
                                model: 'tien.luong.bang.cham.cong.form',
                                method: 'kiem_tra_ton_tai_bang_cham_cong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        dam_bao_check_du_dieu_kien = true;
                                    } else {
                                        dam_bao_check_du_dieu_kien = false;
                                        error = 'Không tồn tại bảng chấm công tương ứng. Xin vui lòng kiểm tra lại.';
                                        self.notifyInvalidFields(error);
                                        def.resolve(false);
                                    }
                                }
                            });
                        }
                        if (dam_bao_check_du_dieu_kien == true) {

                            controller.rpc_action({
                                model: 'tien.luong.tong.hop.cham.cong.tham.so',
                                method: 'kiem_tra_ton_tai_bang_tong_hop_cham_cong',
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
                                                    new dialogs.FormViewDialog(self, {
                                                        res_id: result,
                                                        readonly: false,
                                                        res_model: 'tien.luong.bang.tong.hop.cham.cong',
                                                        ref_views: [
                                                            ['tien_luong.view_tien_luong_bang_tong_hop_cham_cong_form', 'form']
                                                        ],
                                                        title: 'Bảng tổng hợp chấm công',
                                                        disable_multiple_selection: true,
                                                        shouldSaveLocally: false,

                                                    }).open();
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
                        var ten_bang_cham_cong = record.data.TEN_BANG_TONG_HOP_CHAM_CONG;
                        var ten_loai_cham_cong = record.data.tenLoaiChamCong;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET = record.data.TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET;
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
                        var context = {
                            'default_TEN_BANG_CHAM_CONG': ten_bang_cham_cong,
                            'default_THANG': thang,
                            'default_loai_cham_cong': ten_loai_cham_cong,
                            // 'default_LOAI_CHAM_CONG':record.data.LOAI_CHAM_CONG,
                            'default_NAM': nam,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET': TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTongHopBangChamCongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTongHopBangChamCongController,
        }),
    });

    view_registry.add('tien_luong_tong_hop_bang_cham_cong_form_view', TienLuongTongHopBangChamCongView);

    return TienLuongTongHopBangChamCongView;
});

odoo.define('tien_luong.tien_luong_tong_hop_bang_cham_cong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var TienLuongTongHopBangChamCongController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.tong.hop.cham.cong.tham.so',
                readonly: false,
                title: 'Tổng hợp chấm công',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_tong_hop_cham_cong_tham_so_tham_so_form', 'form']
                ],
                size: 'large',
                on_before_saved: function (controller) {
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
                        var thang = controller.getFieldValue('THANG');
                        var nam = controller.getFieldValue('NAM');
                        var dam_bao_check_du_dieu_kien = true;
                        var tong_hop_tu_cac_bang_cham_cong_chi_tiet = controller.getFieldValue('TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET');
                        if (tong_hop_tu_cac_bang_cham_cong_chi_tiet == true) {
                            controller.rpc_action({
                                model: 'tien.luong.bang.cham.cong.form',
                                method: 'kiem_tra_ton_tai_bang_cham_cong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        dam_bao_check_du_dieu_kien = true;
                                    } else {
                                        dam_bao_check_du_dieu_kien = false;
                                        error = 'Không tồn tại bảng chấm công tương ứng. Xin vui lòng kiểm tra lại.';
                                        self.notifyInvalidFields(error);
                                        def.resolve(false);
                                    }
                                }
                            });
                        }
                        if (dam_bao_check_du_dieu_kien == true) {

                            controller.rpc_action({
                                model: 'tien.luong.tong.hop.cham.cong.tham.so',
                                method: 'kiem_tra_ton_tai_bang_tong_hop_cham_cong',
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
                                                    new dialogs.FormViewDialog(self, {
                                                        res_id: result,
                                                        readonly: false,
                                                        res_model: 'tien.luong.bang.tong.hop.cham.cong',
                                                        ref_views: [
                                                            ['tien_luong.view_tien_luong_bang_tong_hop_cham_cong_form', 'form']
                                                        ],
                                                        title: 'Bảng tổng hợp chấm công',
                                                        disable_multiple_selection: true,
                                                        shouldSaveLocally: false,

                                                    }).open();
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
                        var ten_bang_cham_cong = record.data.TEN_BANG_TONG_HOP_CHAM_CONG;
                        var ten_loai_cham_cong = record.data.tenLoaiChamCong;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET = record.data.TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET;
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
                        var context = {
                            'default_TEN_BANG_CHAM_CONG': ten_bang_cham_cong,
                            'default_THANG': thang,
                            'default_loai_cham_cong': ten_loai_cham_cong,
                            // 'default_LOAI_CHAM_CONG':record.data.LOAI_CHAM_CONG,
                            'default_NAM': nam,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET': TONG_HOP_TU_CAC_BANG_CHAM_CONG_CHI_TIET,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTongHopBangChamCongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongTongHopBangChamCongController,
        }),
    });

    view_registry.add('tien_luong_tong_hop_bang_cham_cong_list_view', TienLuongTongHopBangChamCongView);

    return TienLuongTongHopBangChamCongView;
});