odoo.define('gia_thanh.chon_ky_tinh_gia_thanh_nghiem_thu_don_hang_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChonKyTinhGiaThanhNghiemThuDonHangFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so.ten,
				'KY_TINH_GIA_THANH_ID':self.params.tham_so.id_ky_tinh_gia_thanh,
			});
			this.rpc_action({
                model: 'gia.thanh.chon.ky.tinh.gia.thanh.form',
                method: 'lay_du_lieu',
                args: {
                    'ky_tinh_gia_thanh_id' : self.params.ky_tinh_gia_thanh_id,
                    'loai_gia_thanh' : 'DON_HANG',
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
                }
            });

            def.resolve();
        },
    });
    
    var ChonKyTinhGiaThanhNghiemThuDonHangFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ChonKyTinhGiaThanhNghiemThuDonHangFormController,
        }),
    });
    
    view_registry.add('chon_ky_tinh_gia_thanh_nghiem_thu_don_hang_form_view', ChonKyTinhGiaThanhNghiemThuDonHangFormView);
    
    return ChonKyTinhGiaThanhNghiemThuDonHangFormView;
});
