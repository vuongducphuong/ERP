odoo.define('gia_thanh.chon_ky_tinh_gia_thanh_nghiem_thu_hop_dong_form_tham_so_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChonKyTinhGiaThanhNghiemThuHopDongThamSoFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			if (self.params && self.params.tham_so){
					this.getFieldWidget('KY_TINH_GIA_THANH_ID').changeDomain([['LOAI_GIA_THANH','=',self.params.tham_so]]);
			}

            def.resolve();
        },
    });
    
    var ChonKyTinhGiaThanhNghiemThuHopDongThamSoFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ChonKyTinhGiaThanhNghiemThuHopDongThamSoFormController,
        }),
    });
    
    view_registry.add('chon_ky_tinh_gia_thanh_nghiem_thu_hop_dong_form_tham_so_view', ChonKyTinhGiaThanhNghiemThuHopDongThamSoFormView);
    
    return ChonKyTinhGiaThanhNghiemThuHopDongThamSoFormView;
});
