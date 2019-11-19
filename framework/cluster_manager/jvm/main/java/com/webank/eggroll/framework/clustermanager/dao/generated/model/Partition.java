/*
 * Copyright (c) 2019 - now, Eggroll Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 *
 */

package com.webank.eggroll.framework.clustermanager.dao.generated.model;

import java.io.Serializable;
import java.util.Date;

public class Partition implements Serializable {
    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.partition_id
     *
     * @mbg.generated
     */
    private Long partitionId;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.store_id
     *
     * @mbg.generated
     */
    private Long storeId;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.node_id
     *
     * @mbg.generated
     */
    private Long nodeId;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.store_partition_id
     *
     * @mbg.generated
     */
    private String storePartitionId;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.status
     *
     * @mbg.generated
     */
    private String status;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.created_at
     *
     * @mbg.generated
     */
    private Date createdAt;

    /**
     *
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database column partition.updated_at
     *
     * @mbg.generated
     */
    private Date updatedAt;

    /**
     * This field was generated by MyBatis Generator.
     * This field corresponds to the database table partition
     *
     * @mbg.generated
     */
    private static final long serialVersionUID = 1L;

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.partition_id
     *
     * @return the value of partition.partition_id
     *
     * @mbg.generated
     */
    public Long getPartitionId() {
        return partitionId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.partition_id
     *
     * @param partitionId the value for partition.partition_id
     *
     * @mbg.generated
     */
    public void setPartitionId(Long partitionId) {
        this.partitionId = partitionId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.store_id
     *
     * @return the value of partition.store_id
     *
     * @mbg.generated
     */
    public Long getStoreId() {
        return storeId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.store_id
     *
     * @param storeId the value for partition.store_id
     *
     * @mbg.generated
     */
    public void setStoreId(Long storeId) {
        this.storeId = storeId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.node_id
     *
     * @return the value of partition.node_id
     *
     * @mbg.generated
     */
    public Long getNodeId() {
        return nodeId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.node_id
     *
     * @param nodeId the value for partition.node_id
     *
     * @mbg.generated
     */
    public void setNodeId(Long nodeId) {
        this.nodeId = nodeId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.store_partition_id
     *
     * @return the value of partition.store_partition_id
     *
     * @mbg.generated
     */
    public String getStorePartitionId() {
        return storePartitionId;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.store_partition_id
     *
     * @param storePartitionId the value for partition.store_partition_id
     *
     * @mbg.generated
     */
    public void setStorePartitionId(String storePartitionId) {
        this.storePartitionId = storePartitionId == null ? null : storePartitionId.trim();
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.status
     *
     * @return the value of partition.status
     *
     * @mbg.generated
     */
    public String getStatus() {
        return status;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.status
     *
     * @param status the value for partition.status
     *
     * @mbg.generated
     */
    public void setStatus(String status) {
        this.status = status == null ? null : status.trim();
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.created_at
     *
     * @return the value of partition.created_at
     *
     * @mbg.generated
     */
    public Date getCreatedAt() {
        return createdAt;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.created_at
     *
     * @param createdAt the value for partition.created_at
     *
     * @mbg.generated
     */
    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method returns the value of the database column partition.updated_at
     *
     * @return the value of partition.updated_at
     *
     * @mbg.generated
     */
    public Date getUpdatedAt() {
        return updatedAt;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method sets the value of the database column partition.updated_at
     *
     * @param updatedAt the value for partition.updated_at
     *
     * @mbg.generated
     */
    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method corresponds to the database table partition
     *
     * @mbg.generated
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(getClass().getSimpleName());
        sb.append(" [");
        sb.append("Hash = ").append(hashCode());
        sb.append(", partitionId=").append(partitionId);
        sb.append(", storeId=").append(storeId);
        sb.append(", nodeId=").append(nodeId);
        sb.append(", storePartitionId=").append(storePartitionId);
        sb.append(", status=").append(status);
        sb.append(", createdAt=").append(createdAt);
        sb.append(", updatedAt=").append(updatedAt);
        sb.append("]");
        return sb.toString();
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method corresponds to the database table partition
     *
     * @mbg.generated
     */
    @Override
    public boolean equals(Object that) {
        if (this == that) {
            return true;
        }
        if (that == null) {
            return false;
        }
        if (getClass() != that.getClass()) {
            return false;
        }
        Partition other = (Partition) that;
        return (this.getPartitionId() == null ? other.getPartitionId() == null : this.getPartitionId().equals(other.getPartitionId()))
            && (this.getStoreId() == null ? other.getStoreId() == null : this.getStoreId().equals(other.getStoreId()))
            && (this.getNodeId() == null ? other.getNodeId() == null : this.getNodeId().equals(other.getNodeId()))
            && (this.getStorePartitionId() == null ? other.getStorePartitionId() == null : this.getStorePartitionId().equals(other.getStorePartitionId()))
            && (this.getStatus() == null ? other.getStatus() == null : this.getStatus().equals(other.getStatus()))
            && (this.getCreatedAt() == null ? other.getCreatedAt() == null : this.getCreatedAt().equals(other.getCreatedAt()))
            && (this.getUpdatedAt() == null ? other.getUpdatedAt() == null : this.getUpdatedAt().equals(other.getUpdatedAt()));
    }

    /**
     * This method was generated by MyBatis Generator.
     * This method corresponds to the database table partition
     *
     * @mbg.generated
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((getPartitionId() == null) ? 0 : getPartitionId().hashCode());
        result = prime * result + ((getStoreId() == null) ? 0 : getStoreId().hashCode());
        result = prime * result + ((getNodeId() == null) ? 0 : getNodeId().hashCode());
        result = prime * result + ((getStorePartitionId() == null) ? 0 : getStorePartitionId().hashCode());
        result = prime * result + ((getStatus() == null) ? 0 : getStatus().hashCode());
        result = prime * result + ((getCreatedAt() == null) ? 0 : getCreatedAt().hashCode());
        result = prime * result + ((getUpdatedAt() == null) ? 0 : getUpdatedAt().hashCode());
        return result;
    }
}