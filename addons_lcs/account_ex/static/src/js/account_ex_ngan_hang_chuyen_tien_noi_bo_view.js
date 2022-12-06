odoo.define('account_ex.account_ex_ngan_hang_chuyen_tien_noi_bo_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var ChuyenTienNoiBoController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            if (this.getFieldValue('LOAI_PHIEU')=='PHIEU_CHUYEN_TIEN') {
                blackList['01-TT Phiếu thu'] = true;
                blackList['02-TT: Phiếu chi'] = true;
                blackList['Giấy báo có'] = true;
                blackList['02-TT Phiếu chi(Mẫu đầy đủ)'] = true;
                blackList['02-TT Phiếu chi(Mẫu A5)'] = true;
                blackList['02-TT Phiếu chi(Mẫu 2 liên)'] = true;
                blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
            }
            return blackList;
        },
    });
    
    var ChuyenTienNoiBoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChuyenTienNoiBoController,
        }),
    });
    
    view_registry.add('account_ex_ngan_hang_chuyen_tien_noi_bo_form_view', ChuyenTienNoiBoView);
    
    return ChuyenTienNoiBoView;
});

odoo.define('account_ex.account_ex_ngan_hang_chuyen_tien_noi_bo_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var ChuyenTienNoiBoController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.LOAI_PHIEU == 'PHIEU_CHUYEN_TIEN') {
                    blackList['01-TT Phiếu thu'] = true;
                    blackList['02-TT: Phiếu chi'] = true;
                    blackList['Giấy báo có'] = true;
                    blackList['02-TT Phiếu chi(Mẫu đầy đủ)'] = true;
                    blackList['02-TT Phiếu chi(Mẫu A5)'] = true;
                    blackList['02-TT Phiếu chi(Mẫu 2 liên)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
                }
            }
            return blackList;
        },
    });
    
    var ChuyenTienNoiBoView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: ChuyenTienNoiBoController,
        }),
    });
    
    view_registry.add('account_ex_ngan_hang_chuyen_tien_noi_bo_list_view', ChuyenTienNoiBoView);
    
    return ChuyenTienNoiBoView;
});