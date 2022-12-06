odoo.define('account_ex.account_ex_ngan_hang_phieu_thu_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var PhieuThuController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            if (this.getFieldValue('LOAI_PHIEU')=='PHIEU_THU') {
                blackList['01-TT Phiếu thu'] = true;
                blackList['02-TT: Phiếu chi'] = true;
                blackList['Giấy báo nợ'] = true;
                blackList['Ủy nhiệm chi (BIDV)'] = true;
                blackList['02-TT Phiếu chi(Mẫu đầy đủ)'] = true;
                blackList['02-TT Phiếu chi(Mẫu A5)'] = true;
                blackList['02-TT Phiếu chi(Mẫu 2 liên)'] = true;
                blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
                blackList['Uỷ nhiệm chi (Agribank)'] = true;
                blackList['Uỷ nhiệm chi (SHB)'] = true;
                blackList['Uỷ nhiệm chi Viettinbank'] = true;
                blackList['Uỷ nhiệm chi (MB)'] = true;
                blackList['Uỷ nhiệm chi Techcombank'] = true;
                blackList['Uỷ nhiệm chi (Vietcombank)'] = true;
                blackList['Uỷ nhiệm chi (PVC)'] = true;
            }
            return blackList;
        },
    });
    
    var PhieuThuView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhieuThuController,
        }),
    });
    
    view_registry.add('account_ex_ngan_hang_phieu_thu_form_view', PhieuThuView);
    
    return PhieuThuView;
});

odoo.define('account_ex.account_ex_ngan_hang_phieu_thu_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var PhieuThuController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.LOAI_PHIEU == 'PHIEU_THU') {
                    blackList['01-TT Phiếu thu'] = true;
                    blackList['02-TT: Phiếu chi'] = true;
                    blackList['Giấy báo nợ'] = true;
                    blackList['Ủy nhiệm chi (BIDV)'] = true;
                    blackList['02-TT Phiếu chi(Mẫu đầy đủ)'] = true;
                    blackList['02-TT Phiếu chi(Mẫu A5)'] = true;
                    blackList['02-TT Phiếu chi(Mẫu 2 liên)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu đầy đủ)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu A5)'] = true;
                    blackList['01-TT Phiếu thu(Mẫu 2 liên)'] = true;
                    blackList['Uỷ nhiệm chi (Agribank)'] = true;
                    blackList['Uỷ nhiệm chi (SHB)'] = true;
                    blackList['Uỷ nhiệm chi Viettinbank'] = true;
                    blackList['Uỷ nhiệm chi (MB)'] = true;
                    blackList['Uỷ nhiệm chi Techcombank'] = true;
                    blackList['Uỷ nhiệm chi (Vietcombank)'] = true;
                    blackList['Uỷ nhiệm chi (PVC)'] = true;
                }
            }
            return blackList;
        },
    });
    
    var PhieuThuView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PhieuThuController,
        }),
    });
    
    view_registry.add('account_ex_ngan_hang_phieu_thu_list_view', PhieuThuView);
    
    return PhieuThuView;
});