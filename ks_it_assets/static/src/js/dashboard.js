/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class KsItDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        
        this.state = useState({
            stats: {
                total_assets: 0,
                available_assets: 0,
                assigned_assets: 0,
                in_repair: 0,
                active_assignments: 0,
                active_repairs: 0
            }
        });

        onWillStart(async () => {
            await this.fetchData();
        });
    }

    async fetchData() {
        // Fetch Asset Stats
        const assetGroups = await this.orm.readGroup(
            "ks.it.asset",
            [],
            ['status'],
            ['status']
        );
        
        let total = 0;
        let available = 0;
        let assigned = 0;
        let repair = 0;

        assetGroups.forEach(group => {
            total += group.status_count;
            if (group.status === 'available') available = group.status_count;
            if (group.status === 'assigned') assigned = group.status_count;
            if (group.status === 'repair') repair = group.status_count;
        });

        this.state.stats.total_assets = total;
        this.state.stats.available_assets = available;
        this.state.stats.assigned_assets = assigned;
        this.state.stats.in_repair = repair;

        // Fetch active assignments
        this.state.stats.active_assignments = await this.orm.searchCount("ks.it.assignment", [['state', '=', 'active']]);
        
        // Fetch active repairs
        this.state.stats.active_repairs = await this.orm.searchCount("ks.it.repair", [['state', '=', 'in_progress']]);
    }

    openAssets(domain, title) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "ks.it.asset",
            view_mode: "tree,kanban,form",
            views: [[false, "list"], [false, "kanban"], [false, "form"]],
            domain: domain,
            target: "current"
        });
    }

    openAssignments() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Aktif Zimmetler",
            res_model: "ks.it.assignment",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', '=', 'active']],
            target: "current"
        });
    }

    openRepairs() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "İşlemdeki Tamirler",
            res_model: "ks.it.repair",
            view_mode: "tree,form",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', '=', 'in_progress']],
            target: "current"
        });
    }
}

KsItDashboard.template = "ks_it_assets.Dashboard_Premium";
registry.category("actions").add("ks_it_assets_dashboard", KsItDashboard);
